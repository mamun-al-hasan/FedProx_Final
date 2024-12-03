bash run_fedprox_auto_mu_lr.sh synthetic_iid 0 1 0.1 | tee log_synthetic/auto_tune_lr_0.1_synthetic_iid_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_iid 0 1 0.2 | tee log_synthetic/auto_tune_lr_0.2_synthetic_iid_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_iid 0 1 0.5 | tee log_synthetic/auto_tune_lr_0.5_synthetic_iid_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_iid 0 1 1 | tee log_synthetic/auto_tune_lr_1_synthetic_iid_client10_epoch20_mu_changing

bash run_fedprox_auto_mu_lr.sh synthetic_0_0 0 1 0.1 | tee log_synthetic/auto_tune_lr_0.1_synthetic_0_0_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_0_0 0 1 0.2 | tee log_synthetic/auto_tune_lr_0.2_synthetic_0_0_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_0_0 0 1 0.5 | tee log_synthetic/auto_tune_lr_0.5_synthetic_0_0_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_0_0 0 1 1 | tee log_synthetic/auto_tune_lr_1_synthetic_0_0_client10_epoch20_mu_changing

bash run_fedprox_auto_mu_lr.sh synthetic_0.5_0.5 0 1 0.1 | tee log_synthetic/auto_tune_lr_0.1_synthetic_0.5_0.5_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_0.5_0.5 0 1 0.2 | tee log_synthetic/auto_tune_lr_0.2_synthetic_0.5_0.5_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_0.5_0.5 0 1 0.5 | tee log_synthetic/auto_tune_lr_0.5_synthetic_0.5_0.5_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_0.5_0.5 0 1 1 | tee log_synthetic/auto_tune_lr_1_synthetic_0.5_0.5_client10_epoch20_mu_changing

bash run_fedprox_auto_mu_lr.sh synthetic_1_1 0 1 0.1 | tee log_synthetic/auto_tune_lr_0.1_synthetic_1_1_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_1_1 0 1 0.2 | tee log_synthetic/auto_tune_lr_0.2_synthetic_1_1_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_1_1 0 1 0.5 | tee log_synthetic/auto_tune_lr_0.5_synthetic_1_1_client10_epoch20_mu_changing
bash run_fedprox_auto_mu_lr.sh synthetic_1_1 0 1 1 | tee log_synthetic/auto_tune_lr_1_synthetic_1_1_client10_epoch20_mu_changing