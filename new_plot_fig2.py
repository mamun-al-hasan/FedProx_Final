import os
import sys
import re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Configure matplotlib for consistent, large font sizes
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

def plot_experiments(metric='loss', log_types=None):
    """
    Create visualization for multiple experiments and mu values, saving as individual PNG files.
    
    Args:
        metric (str): Type of metric to plot ('loss', 'accuracy', or 'similarity')
        log_types (list): List of log type prefixes to process
    """

    # Default log types if not specified
    if log_types is None:
        log_types = ["synthetic_iid", "synthetic_0_0", "synthetic_0.5_0.5", "synthetic_1_1"]
    
    # Color palette for different mu values
    colors = ['#17becf', '#e377c2', '#7f7f7f', '#bcbd22', '#9467bd', '#8c564b']
    
    # Create a separate figure for each log type
    for log in log_types:
        plt.figure(figsize=(10, 6))
        
        # Prepare to store data for all mu values
        all_rounds = []
        all_values = []
        labels = []
        
        # Find and plot data for mu values 0 to 5
        for mu in range(6):
            try:
                file_path = f"log_synthetic/{log}_client10_epoch20_mu{mu}"
                rounds_data, sim_data, loss_data, accu_data = parse_log(file_path)
                
                # Select metric to plot
                if metric == 'loss':
                    values = loss_data
                    ylabel = 'Training Loss'
                    filename_metric = 'loss'
                elif metric == 'accuracy':
                    values = accu_data
                    ylabel = 'Testing Accuracy'
                    filename_metric = 'accuracy'
                else:  # similarity/gradient difference
                    values = sim_data
                    ylabel = "Variance of Local Grad."
                    filename_metric = 'similarity'
                
                # Plot if data exists
                if values:
                    plt.plot(np.asarray(rounds_data[:len(values)]), 
                             np.asarray(values), 
                             linewidth=3.0, 
                             label=f'μ={mu}, E=20', 
                             color=colors[mu],
                             linestyle='--' if mu % 2 == 0 else '-')
            
            except Exception as e:
                print(f"Error processing {log} with mu={mu}: {e}")
        
        # Styling
        plt.xlabel("# Rounds", fontsize=22)
        plt.ylabel(ylabel, fontsize=22)
        plt.title(f"{log} - {ylabel}", fontsize=22)
        
        # Spine and tick styling
        plt.gca().spines['bottom'].set_color('#dddddd')
        plt.gca().spines['top'].set_color('#dddddd')
        plt.gca().spines['right'].set_color('#dddddd')
        plt.gca().spines['left'].set_color('#dddddd')
        
        plt.gca().tick_params(color='#dddddd')
        
        # Add legend
        plt.legend(fontsize=14, loc='best')
        
        # Ensure output directory exists
        os.makedirs('output_plots', exist_ok=True)
        
        # Save as PNG
        output_filename = f'output_plots/{log}_{filename_metric}_multi_mu.png'
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        plt.close()

def main():
    """Main function to handle command-line arguments and trigger plotting"""
    # Default to loss if no argument provided
    metric = sys.argv[1] if len(sys.argv) > 1 else 'loss'
    
    # Supported metrics
    supported_metrics = ['loss', 'accuracy', 'similarity']
    
    if metric not in supported_metrics:
        print(f"Invalid metric. Choose from: {', '.join(supported_metrics)}")
        sys.exit(1)
    
    plot_experiments(metric)

if __name__ == "__main__":
    main()