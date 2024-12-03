import os, sys
import re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib import rcParams
from mpl_toolkits.axisartist.axislines import Subplot

from plot_fig2_auto_tune_lr import losses

matplotlib.rc('xtick', labelsize=17)
matplotlib.rc('ytick', labelsize=17)


def parse_log(file_name):
    rounds = []
    accu = []
    loss = []
    sim = []

    for line in open(file_name, 'r'):

        search_train_accu = re.search(r'At round (.*) training accuracy: (.*)', line, re.M | re.I)
        if search_train_accu:
            rounds.append(int(search_train_accu.group(1)))
        else:
            search_test_accu = re.search(r'At round (.*) accuracy: (.*)', line, re.M | re.I)
            if search_test_accu:
                accu.append(float(search_test_accu.group(2)))

        search_loss = re.search(r'At round (.*) training loss: (.*)', line, re.M | re.I)
        if search_loss:
            loss.append(float(search_loss.group(2)))

        search_loss = re.search(r'gradient difference: (.*)', line, re.M | re.I)
        if search_loss:
            sim.append(float(search_loss.group(1)))

    return rounds, sim, loss, accu

for log in ["synthetic_iid", "synthetic_0_0", "synthetic_0.5_0.5", "synthetic_1_1"]:
    rounds_ = [1, 2, 3, 4, 5]
    fig, axes = plt.subplots(1, 6, figsize=(20, 4))
    index_ = 0
    for r in rounds_:
        rounds, sim, losses, test_accuracies = parse_log("log_synthetic/" + log + "_client10_epoch20_mu" + str(r))

        # print(losses)

        if sys.argv[1] == 'loss':
            axes[index_].plot(np.asarray(rounds[:len(losses)]), np.asarray(losses), '--', linewidth=3.0,
                              label='mu=' + str(round) + ', E=20',
                              color="#17becf")
            axes[index_].set_ylabel(str(r), fontsize=22)
        elif sys.argv[1] == 'accuracy':
            axes[index_].plot(np.asarray(rounds[:len(test_accuracies)], dtype=int), np.asarray(test_accuracies), '--',
                              linewidth=3.0,
                              label='mu=' + str(round) + ', E=20', color="#17becf")
            axes[index_].set_ylabel(str(r),fontsize=22)
        else:
            axes[index_].plot(np.asarray(rounds[:len(sim)], dtype=int), np.asarray(sim), '--', linewidth=3.0,
                              label='mu=' + str(round) + ', E=20',
                              color="#17becf")
            axes[index_].set_ylabel(str(r), fontsize=22)

        index_ += 1

        plt.xlabel("# Rounds", fontsize=22)
        plt.xticks(fontsize=17)
        plt.yticks(fontsize=17)
        plt.title(log, fontsize=22)

        # y label
        if index_ == 1:
            plt.ylabel(sys.argv[1], fontsize=22)
        else:
            plt.yticks([])

        plt.tight_layout()
        plt.show()

        # save the plot
        plt.savefig("fig2_" + sys.argv[1] + "_" + log + ".png")
