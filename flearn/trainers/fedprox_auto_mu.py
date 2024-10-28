import numpy as np
from tqdm import trange, tqdm
import tensorflow as tf

from .fedbase import BaseFederated
from flearn.optimizer.pgd import PerturbedGradientDescent
from flearn.utils.tf_utils import process_grad, process_sparse_grad


class Server(BaseFederated):
    def __init__(self, params, learner, dataset):
        print('Using Federated prox to Train')
        self.inner_opt = PerturbedGradientDescent(params['learning_rate'], params['mu'])
        super(Server, self).__init__(params, learner, dataset)
        
        # Initialize parameters for auto-tuning of μ
        self.mu = params['mu']
        self.eta_mu = 0.01  # Learning rate for updating μ
        self.G_mu = 0  # Initial accumulated gradient for μ
        self.epsilon = 1e-8  # Small constant to avoid division by zero in AdaGrad

    def train(self):
        '''Train using Federated Proximal with auto-tuning for μ'''
        print('Training with {} workers ---'.format(self.clients_per_round))

        for i in range(self.num_rounds):
            # test model
            if i % self.eval_every == 0:
                stats = self.test()  # have set the latest model for all clients
                stats_train = self.train_error_and_loss()

                tqdm.write(
                    'At round {} accuracy: {}'.format(i, np.sum(stats[3]) * 1.0 / np.sum(stats[2])))  # testing accuracy
                tqdm.write('At round {} training accuracy: {}'.format(i, np.sum(stats_train[3]) * 1.0 / np.sum(
                    stats_train[2])))
                tqdm.write('At round {} training loss: {}'.format(i,
                                                                  np.dot(stats_train[4], stats_train[2]) * 1.0 / np.sum(
                                                                      stats_train[2])))

            model_len = process_grad(self.latest_model).size
            global_grads = np.zeros(model_len)
            client_grads = np.zeros(model_len)
            num_samples = []
            local_grads = []

            # Collect gradients from clients
            for c in self.clients:
                num, client_grad = c.get_grads(model_len)
                local_grads.append(client_grad)
                num_samples.append(num)
                global_grads = np.add(global_grads, client_grad * num)
            global_grads = global_grads * 1.0 / np.sum(np.asarray(num_samples))

            # Compute gradient difference and use it to auto-tune μ
            gradient_diff = 0
            for idx in range(len(self.clients)):
                gradient_diff += np.sum(np.square(global_grads - local_grads[idx]))
            gradient_diff /= len(self.clients)
            
            # Auto-tune μ using AdaGrad
            grad_mu = gradient_diff
            self.G_mu += grad_mu ** 2
            self.mu += self.eta_mu * grad_mu / (np.sqrt(self.G_mu) + self.epsilon)
            tqdm.write(f'Updated μ: {self.mu}, Gradient difference: {gradient_diff}')

            indices, selected_clients = self.select_clients(i, num_clients=self.clients_per_round)  # uniform sampling
            np.random.seed(i)  # make sure that the stragglers are the same for FedProx and FedAvg
            active_clients = np.random.choice(selected_clients, round(self.clients_per_round * (1 - self.drop_percent)),
                                              replace=False)

            csolns = []  # buffer for receiving client solutions

            # Set μ in the optimizer
            self.inner_opt.mu = self.mu
            self.inner_opt.set_params(self.latest_model, self.client_model)

            # Perform local updates and aggregate solutions
            for idx, c in enumerate(selected_clients.tolist()):
                # communicate the latest model
                c.set_params(self.latest_model)

                total_iters = int(self.num_epochs * c.num_samples / self.batch_size) + 2  # randint(low,high)=[low,high)

                # solve minimization locally
                if c in active_clients:
                    soln, stats = c.solve_inner(num_epochs=self.num_epochs, batch_size=self.batch_size)
                else:
                    soln, stats = c.solve_inner(num_epochs=np.random.randint(low=1, high=self.num_epochs),
                                                batch_size=self.batch_size)

                # gather solutions from client
                csolns.append(soln)

                # track communication cost
                self.metrics.update(rnd=i, cid=c.id, stats=stats)

            # update models
            self.latest_model = self.aggregate(csolns)
            self.client_model.set_params(self.latest_model)

        # Final test model
        stats = self.test()
        stats_train = self.train_error_and_loss()
        self.metrics.accuracies.append(stats)
        self.metrics.train_accuracies.append(stats_train)
        tqdm.write('At round {} accuracy: {}'.format(self.num_rounds, np.sum(stats[3]) * 1.0 / np.sum(stats[2])))
        tqdm.write('At round {} training accuracy: {}'.format(self.num_rounds,
                                                              np.sum(stats_train[3]) * 1.0 / np.sum(stats_train[2])))
