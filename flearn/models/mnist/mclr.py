import numpy as np
import tensorflow as tf
import keras
from keras import regularizers
from tqdm import trange

from flearn.utils.model_utils import batch_data, batch_data_multiple_iters
from flearn.utils.tf_utils import graph_size, process_grad

class Model(object):
    def __init__(self, num_classes, optimizer, seed=1):
        self.num_classes = num_classes
        self.graph = tf.Graph()

        with self.graph.as_default():
            tf.random.set_seed(seed+123)
            self.features, self.labels, self.train_op, self.grads, self.eval_metric_ops, self.loss = self.create_model(optimizer)
            self.saver = tf.compat.v1.train.Saver()
        self.sess = tf.compat.v1.Session(graph=self.graph)
        self.size = graph_size(self.graph)
        with self.graph.as_default():
            self.sess.run(tf.compat.v1.global_variables_initializer())
            metadata = tf.compat.v1.RunMetadata()
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
            self.flops = tf.compat.v1.profiler.profile(self.graph, run_meta=metadata, cmd='scope', options=opts).total_float_ops

    def create_model(self, optimizer):
        features = tf.compat.v1.placeholder(tf.float32, shape=[None, 784], name='features')
        labels = tf.compat.v1.placeholder(tf.int64, shape=[None, ], name='labels')
        logits_input = keras.layers.Dense(units=self.num_classes,
                                 kernel_regularizer=regularizers.L2(0.001))
        logits = logits_input(features)
        predictions = {
            "classes": tf.argmax(input=logits, axis=1),
            "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
        }
        loss = tf.compat.v1.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

        grads_and_vars = optimizer.compute_gradients(loss)
        grads, _ = zip(*grads_and_vars)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=tf.compat.v1.train.get_global_step())
        eval_metric_ops = tf.compat.v1.count_nonzero(tf.equal(labels, predictions["classes"]))
        return features, labels, train_op, grads, eval_metric_ops, loss

    def set_params(self, model_params=None):
        if model_params is not None:
            with self.graph.as_default():
                all_vars = tf.compat.v1.trainable_variables()
                for variable, value in zip(all_vars, model_params):
                    variable.load(value, self.sess)

    def get_params(self):
        with self.graph.as_default():
            model_params = self.sess.run(tf.compat.v1.trainable_variables())
        return model_params

    def get_gradients(self, data, model_len):

        grads = np.zeros(model_len)
        num_samples = len(data['y'])

        with self.graph.as_default():
            model_grads = self.sess.run(self.grads,
                                        feed_dict={self.features: data['x'], self.labels: data['y']})
            grads = process_grad(model_grads)

        return num_samples, grads

    def solve_inner(self, data, num_epochs=1, batch_size=32):
        for _ in trange(num_epochs, desc='Epoch: ', leave=False, ncols=120):
            for X, y in batch_data(data, batch_size):
                with self.graph.as_default():
                    self.sess.run(self.train_op,
                                  feed_dict={self.features: X, self.labels: y})
        solution = self.get_params()
        comp = num_epochs * (len(data['y']) // batch_size) * batch_size * self.flops
        return solution, comp

    def solve_iters(self, data, num_iters=1, batch_size=32):
        for X, y in batch_data_multiple_iters(data, batch_size, num_iters):
            with self.graph.as_default():
                self.sess.run(self.train_op, feed_dict={self.features: X, self.labels: y})
        solution = self.get_params()
        comp = 0
        return solution, comp

    def test(self, data):
        with self.graph.as_default():
            tot_correct, loss = self.sess.run([self.eval_metric_ops, self.loss],
                                              feed_dict={self.features: data['x'], self.labels: data['y']})
        return tot_correct, loss

    def close(self):
        self.sess.close()
