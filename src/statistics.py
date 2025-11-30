"""
Statistics tracking for performance analysis.
"""

import threading
import time
import csv
import os
from datetime import datetime


class Statistics:
    """Track and log statistics for performance analysis."""
    
    def __init__(self, node_id, log_dir='logs'):
        self.node_id = node_id
        self.log_dir = log_dir
        
        # Counters
        self.queries_received = 0
        self.queries_forwarded = 0
        self.queries_answered = 0
        self.messages_sent = 0
        self.messages_received = 0
        
        # Performance metrics
        self.hops_list = []
        self.latencies = []
        
        self.lock = threading.Lock()
        
        # Create logs directory
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'node_{node_id}.csv')
        
        # Initialize CSV log
        self._init_log()
    
    def _init_log(self):
        """Initialize CSV log file."""
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'event_type', 'query', 'hops', 
                'latency_ms', 'sender_ip', 'sender_port'
            ])
    
    def log_event(self, event_type, query='', hops=0, latency_ms=0, 
                   sender_ip='', sender_port=''):
        """Log an event to CSV file."""
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                event_type,
                query,
                hops,
                latency_ms,
                sender_ip,
                sender_port
            ])
    
    def record_query_received(self):
        """Record that a query was received."""
        with self.lock:
            self.queries_received += 1
            self.messages_received += 1
    
    def record_query_forwarded(self):
        """Record that a query was forwarded."""
        with self.lock:
            self.queries_forwarded += 1
            self.messages_sent += 1
    
    def record_query_answered(self):
        """Record that a query was answered."""
        with self.lock:
            self.queries_answered += 1
            self.messages_sent += 1
    
    def record_message_sent(self):
        """Record a message sent."""
        with self.lock:
            self.messages_sent += 1
    
    def record_message_received(self):
        """Record a message received."""
        with self.lock:
            self.messages_received += 1
    
    def record_hop(self, hop_count):
        """Record hop count for a query."""
        with self.lock:
            self.hops_list.append(hop_count)
    
    def record_latency(self, latency_ms):
        """Record latency for a query."""
        with self.lock:
            self.latencies.append(latency_ms)
    
    def get_stats(self):
        """Get current statistics."""
        with self.lock:
            return {
                'queries_received': self.queries_received,
                'queries_forwarded': self.queries_forwarded,
                'queries_answered': self.queries_answered,
                'messages_sent': self.messages_sent,
                'messages_received': self.messages_received
            }
    
    def save_summary(self):
        """Save summary stats to a separate CSV file."""
        stats = self.get_stats()
        summary_file = os.path.join(self.log_dir, f'node_{self.node_id}_summary.csv')
        try:
            with open(summary_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['metric', 'value'])
                for k, v in stats.items():
                    writer.writerow([k, v])
        except Exception as e:
            print(f"Error saving summary: {e}")
    
    def save_to_csv(self):
        """Alias for save_summary for compatibility."""
        return self.save_summary()

    def print_stats(self):
        """Print current statistics."""
        stats = self.get_stats()
        print("\n=== Node Statistics ===")
        print(f"Queries Received:  {stats['queries_received']}")
        print(f"Queries Forwarded: {stats['queries_forwarded']}")
        print(f"Queries Answered:  {stats['queries_answered']}")
        print(f"Messages Sent:     {stats['messages_sent']}")
        print(f"Messages Received: {stats['messages_received']}")
        
        # Calculate latency and hops stats from log file
        latencies = []
        hops_list = []
        
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['event_type'] == 'SEARCH_RESULT':
                            try:
                                latencies.append(float(row['latency_ms']))
                                hops_list.append(int(row['hops']))
                            except ValueError:
                                continue
            
            if latencies:
                print("\n--- Performance Metrics ---")
                avg_lat = sum(latencies)/len(latencies)
                print(f"Latency (ms): Min={min(latencies):.2f}, Max={max(latencies):.2f}, Avg={avg_lat:.2f}")
                
                if len(latencies) > 1:
                    variance = sum((x - avg_lat) ** 2 for x in latencies) / (len(latencies) - 1)
                    std_dev = variance ** 0.5
                    print(f"Latency StdDev: {std_dev:.2f}")
            
            if hops_list:
                avg_hops = sum(hops_list)/len(hops_list)
                print(f"Hops:         Min={min(hops_list)}, Max={max(hops_list)}, Avg={avg_hops:.2f}")
                
        except Exception as e:
            print(f"Error calculating stats: {e}")
            
        print("=====================\n")
