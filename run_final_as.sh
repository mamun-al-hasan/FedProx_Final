bash run_fedprox.sh mnist 0 1 | tee final_output/mnist_client10_epoch20_mu1
bash run_fedprox.sh mnist 0 2 | tee final_output/mnist_client10_epoch20_mu2
bash run_fedprox.sh mnist 0 3 | tee final_output/mnist_client10_epoch20_mu3
bash run_fedprox.sh mnist 0 4 | tee final_output/mnist_client10_epoch20_mu4

bash run_fedprox.sh synthetic_iid 0 1 | tee final_output/synthetic_iid_client10_epoch20_mu1
bash run_fedprox.sh synthetic_iid 0 2 | tee final_output/synthetic_iid_client10_epoch20_mu2
bash run_fedprox.sh synthetic_iid 0 3 | tee final_output/synthetic_iid_client10_epoch20_mu3
bash run_fedprox.sh synthetic_iid 0 4 | tee final_output/synthetic_iid_client10_epoch20_mu4

bash run_fedprox.sh synthetic_0_0 0 1 | tee final_output/synthetic_0_0_client10_epoch20_mu1
bash run_fedprox.sh synthetic_0_0 0 2 | tee final_output/synthetic_0_0_client10_epoch20_mu2
bash run_fedprox.sh synthetic_0_0 0 3 | tee final_output/synthetic_0_0_client10_epoch20_mu3
bash run_fedprox.sh synthetic_0_0 0 4 | tee final_output/synthetic_0_0_client10_epoch20_mu4

bash run_fedprox.sh synthetic_0.5_0.5 0 1 | tee final_output/synthetic_0.5_0.5_client10_epoch20_mu1
bash run_fedprox.sh synthetic_0.5_0.5 0 2 | tee final_output/synthetic_0.5_0.5_client10_epoch20_mu2
bash run_fedprox.sh synthetic_0.5_0.5 0 3 | tee final_output/synthetic_0.5_0.5_client10_epoch20_mu3
bash run_fedprox.sh synthetic_0.5_0.5 0 4 | tee final_output/synthetic_0.5_0.5_client10_epoch20_mu4

bash run_fedprox.sh synthetic_1_1 0 1 | tee final_output/synthetic_1_1_client10_epoch20_mu1
bash run_fedprox.sh synthetic_1_1 0 2 | tee final_output/synthetic_1_1_client10_epoch20_mu2
bash run_fedprox.sh synthetic_1_1 0 3 | tee final_output/synthetic_1_1_client10_epoch20_mu3
bash run_fedprox.sh synthetic_1_1 0 4 | tee final_output/synthetic_1_1_client10_epoch20_mu4