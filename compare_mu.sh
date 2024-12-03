#Effect of mu on synthetic data

bash run_fedprox.sh synthetic_iid 0 1 | tee log_synthetic/synthetic_iid_client10_epoch20_mu1
bash run_fedprox.sh synthetic_iid 0 2 | tee log_synthetic/synthetic_iid_client10_epoch20_mu2
bash run_fedprox.sh synthetic_iid 0 3 | tee log_synthetic/synthetic_iid_client10_epoch20_mu3
bash run_fedprox.sh synthetic_iid 0 4 | tee log_synthetic/synthetic_iid_client10_epoch20_mu4
bash run_fedprox.sh synthetic_iid 0 5 | tee log_synthetic/synthetic_iid_client10_epoch20_mu5


bash run_fedprox.sh synthetic_0_0 0 1 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu1
bash run_fedprox.sh synthetic_0_0 0 2 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu2
bash run_fedprox.sh synthetic_0_0 0 3 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu3
bash run_fedprox.sh synthetic_0_0 0 4 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu4
bash run_fedprox.sh synthetic_0_0 0 5 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu5

bash run_fedprox.sh synthetic_0.5_0.5 0 1 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu1
bash run_fedprox.sh synthetic_0.5_0.5 0 2 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu2
bash run_fedprox.sh synthetic_0.5_0.5 0 3 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu3
bash run_fedprox.sh synthetic_0.5_0.5 0 4 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu4
bash run_fedprox.sh synthetic_0.5_0.5 0 5 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu5

bash run_fedprox.sh synthetic_1_1 0 1 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu1
bash run_fedprox.sh synthetic_1_1 0 2 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu2
bash run_fedprox.sh synthetic_1_1 0 3 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu3
bash run_fedprox.sh synthetic_1_1 0 4 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu4
bash run_fedprox.sh synthetic_1_1 0 5 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu5