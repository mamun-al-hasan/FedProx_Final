bash run_fedavg.sh synthetic_iid 0 | tee log_synthetic/synthetic_iid_client10_epoch20_mu0
bash run_fedprox.sh synthetic_iid 0 1 | tee log_synthetic/synthetic_iid_client10_epoch20_mu1
bash run_fedavg.sh synthetic_0_0 0 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu0
bash run_fedprox.sh synthetic_0_0 0 1 | tee log_synthetic/synthetic_0_0_client10_epoch20_mu1
bash run_fedavg.sh synthetic_0.5_0.5 0 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu0
bash run_fedprox.sh synthetic_0.5_0.5 0 1 | tee log_synthetic/synthetic_0.5_0.5_client10_epoch20_mu1
bash run_fedavg.sh synthetic_1_1 0 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu0
bash run_fedprox.sh synthetic_1_1 0 1 | tee log_synthetic/synthetic_1_1_client10_epoch20_mu1