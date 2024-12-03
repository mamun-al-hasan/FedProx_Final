import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

def parse_log(file_name):
    """Parse training log file to extract metrics."""
    data = {'rounds': [], 'accuracy': [], 'loss': [], 'gradient_diff': []}
    
    patterns = {
        'train_round': r'At round (.*) training accuracy: (.*)',
        'test_accuracy': r'At round (.*) accuracy: (.*)',
        'train_loss': r'At round (.*) training loss: (.*)',
        'grad_diff': r'gradient difference: (.*)'
    }
    
    with open(file_name, 'r') as f:
        for line in f:
            if match := re.search(patterns['train_round'], line, re.M | re.I):
                data['rounds'].append(int(match.group(1)))
            elif match := re.search(patterns['test_accuracy'], line, re.M | re.I):
                data['accuracy'].append(float(match.group(2)))
            elif match := re.search(patterns['train_loss'], line, re.M | re.I):
                data['loss'].append(float(match.group(2)))
            elif match := re.search(patterns['grad_diff'], line, re.M | re.I):
                data['gradient_diff'].append(float(match.group(1)))
    
    return data

def create_single_plot(data_type, metric_type='loss'):
    """Create a plot for a single dataset."""
    # Set basic style parameters
    plt.style.use('classic')
    rcParams['axes.grid'] = True
    rcParams['grid.alpha'] = 0.3
    
    fig = plt.figure(figsize=[10, 8])
    ax = plt.subplot(111)
    
    learning_rates = ["0.1", "0.2", "0.5", "1"]
    colors = ["#17becf", "#e377c2", "#ff7f0e", "#9467bd"]
    
    metric_configs = {
        'loss': {'label': 'Training Loss', 'key': 'loss'},
        'accuracy': {'label': 'Testing Accuracy', 'key': 'accuracy'},
        'gradient': {'label': 'Variance of Local Grad.', 'key': 'gradient_diff'}
    }
    
    max_values = []  # Store maximum values for the metric
    
    for lr_idx, lr in enumerate(learning_rates):
        filename = f"log_synthetic/auto_tune_lr_{lr}_{data_type}_client10_epoch20_mu_changing"
        try:
            data = parse_log(filename)
            
            metric_key = metric_configs[metric_type]['key']
            metric_data = data[metric_key]
            max_values.append(max(metric_data))  # Store maximum value
            rounds = data['rounds'][:len(metric_data)]
            
            plt.plot(np.asarray(rounds), np.asarray(metric_data),
                    '--' if lr_idx % 2 == 0 else '-',
                    linewidth=3.0,
                    label=f'mu=1, E=20, lr={lr}',
                    color=colors[lr_idx])
        except FileNotFoundError:
            print(f"Warning: Could not find file {filename}")
            continue
    
    fixed_mu_filename = f"log_synthetic/{data_type}_client10_epoch20_mu1"

    try:
        fixed_mu_data = parse_log(fixed_mu_filename)
        fixed_mu_metric = fixed_mu_data[metric_configs[metric_type]['key']]
        plt.plot(np.asarray(fixed_mu_data['rounds'][:len(fixed_mu_metric)]),
                 np.asarray(fixed_mu_metric),
                 '-',
                 linewidth=3.0,
                 label='mu=1, E=20',
                 color='#2ca02c')
    except FileNotFoundError:
        print(f"Warning: Could not find file {fixed_mu_filename}")
    
    plt.xlabel("# Rounds", fontsize=22)
    plt.ylabel(metric_configs[metric_type]['label'], fontsize=22)
    plt.title(f"{data_type} - {metric_configs[metric_type]['label']}", fontsize=22)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    
    # Style the plot
    for spine in ax.spines.values():
        spine.set_color('#dddddd')
    
    plt.legend(fontsize=16, loc='best')
    plt.tight_layout()
    
    # Create output directory if it doesn't exist
    os.makedirs('plots', exist_ok=True)
    
    # Create filename with all information
    lr_string = '_'.join(learning_rates)
    max_metric = max(max_values) if max_values else 0
    min_metric = min(metric_data) if metric_data else 0
    
    output_file = (f"plots/{data_type}_{metric_type}_"
                  f"max_{max_metric:.3f}_min_{min_metric:.3f}_"
                  f"lr_{lr_string}.png")
    
    fig.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close(fig)  # Close the figure to free memory
    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['loss', 'accuracy', 'gradient']:
        print("Usage: python script.py [loss|accuracy|gradient]")
        sys.exit(1)
    
    data_types = ["synthetic_iid", "synthetic_0_0", "synthetic_0.5_0.5", "synthetic_1_1"]
    metric_type = sys.argv[1]
    
    print(f"Generating plots for {metric_type}...")
    for data_type in data_types:
        output_file = create_single_plot(data_type, metric_type)
        print(f"Created: {output_file}")