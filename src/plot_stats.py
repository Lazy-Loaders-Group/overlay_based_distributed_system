import matplotlib.pyplot as plt
import csv
import os
import glob
import numpy as np

def calculate_statistics(data):
    """Calculate min, max, average, and standard deviation."""
    if not data:
        return None
    
    data_array = np.array(data)
    return {
        'min': np.min(data_array),
        'max': np.max(data_array),
        'mean': np.mean(data_array),
        'avg': np.mean(data_array),  # alias
        'std': np.std(data_array),
        'std_dev': np.std(data_array),  # alias
        'median': np.median(data_array)
    }

def plot_cdf(data, label, filename):
    """Plot CDF of data."""
    if not data:
        print(f"No data for {label}")
        return
        
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    
    plt.figure()
    plt.plot(sorted_data, yvals)
    plt.title(f'CDF of {label}')
    plt.xlabel(label)
    plt.ylabel('CDF')
    plt.grid(True)
    plt.savefig(filename)
    print(f"Saved {filename}")
    plt.close()

def main():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        print(f"Log directory '{log_dir}' not found.")
        return

    latencies = []
    hops_list = []
    messages_per_node = []
    
    log_files = glob.glob(os.path.join(log_dir, 'node_*.csv'))
    
    for log_file in log_files:
        node_msgs = 0
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Count messages (sent + received)
                # We can approximate by looking at events or if we logged message counts periodically
                # The current logging logs events.
                # Statistics class tracks total messages.
                # But the CSV log mainly tracks SEARCH_RESULT.
                # To get total messages per node, we might need to read the final stats printed or log them.
                # Currently, the CSV doesn't log total message counts.
                # However, we can extract latency and hops from SEARCH_RESULT events.
                
                if row['event_type'] == 'SEARCH_RESULT':
                    try:
                        latencies.append(float(row['latency_ms']))
                        hops_list.append(int(row['hops']))
                    except ValueError:
                        continue
        
    # Read summary files for messages per node
    summary_files = glob.glob(os.path.join(log_dir, 'node_*_summary.csv'))
    for summary_file in summary_files:
        try:
            msgs_sent = 0
            msgs_received = 0
            with open(summary_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['metric'] == 'messages_sent':
                        msgs_sent = int(row['value'])
                    elif row['metric'] == 'messages_received':
                        msgs_received = int(row['value'])
            messages_per_node.append(msgs_sent + msgs_received)
        except Exception as e:
            print(f"Error reading {summary_file}: {e}")
    
    # Plot CDFs
    plot_cdf(latencies, 'Latency (ms)', 'cdf_latency.png')
    plot_cdf(hops_list, 'Hops', 'cdf_hops.png')
    plot_cdf(messages_per_node, 'Messages per Node', 'cdf_messages.png')
    
    # Print statistics
    print("\n=== Overall Statistics ===")
    if latencies:
        lat_stats = calculate_statistics(latencies)
        print(f"Latency (ms): Min={lat_stats['min']:.2f}, Max={lat_stats['max']:.2f}, "
              f"Avg={lat_stats['avg']:.2f}, StdDev={lat_stats['std']:.2f}")
    
    if hops_list:
        hop_stats = calculate_statistics(hops_list)
        print(f"Hops: Min={hop_stats['min']:.0f}, Max={hop_stats['max']:.0f}, "
              f"Avg={hop_stats['avg']:.2f}, StdDev={hop_stats['std']:.2f}")
    
    if messages_per_node:
        msg_stats = calculate_statistics(messages_per_node)
        print(f"Messages per Node: Min={msg_stats['min']:.0f}, Max={msg_stats['max']:.0f}, "
              f"Avg={msg_stats['avg']:.2f}, StdDev={msg_stats['std']:.2f}")
    print("========================\n")

if __name__ == '__main__':
    main()
