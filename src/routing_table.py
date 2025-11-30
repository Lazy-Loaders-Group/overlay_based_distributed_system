"""
Routing table management for distributed nodes.
"""

import threading
from datetime import datetime


class RoutingTable:
    """Manages neighbor nodes in the distributed system."""
    
    def __init__(self):
        self.neighbors = []
        self.lock = threading.Lock()
    
    def add_neighbor(self, ip, port):
        """
        Add a neighbor to the routing table.
        
        Args:
            ip (str): IP address of neighbor
            port (int): Port number of neighbor
            
        Returns:
            bool: True if added, False if already exists
        """
        with self.lock:
            # Check if already exists
            for neighbor in self.neighbors:
                if neighbor['ip'] == ip and neighbor['port'] == port:
                    return False
            
            self.neighbors.append({
                'ip': ip,
                'port': port,
                'added_at': datetime.now()
            })
            return True
    
    def remove_neighbor(self, ip, port):
        """
        Remove a neighbor from the routing table.
        
        Args:
            ip (str): IP address of neighbor
            port (int): Port number of neighbor
            
        Returns:
            bool: True if removed, False if not found
        """
        with self.lock:
            for i, neighbor in enumerate(self.neighbors):
                if neighbor['ip'] == ip and neighbor['port'] == port:
                    del self.neighbors[i]
                    return True
            return False
    
    def get_neighbors(self):
        """
        Get list of all neighbors.
        
        Returns:
            list: Copy of neighbors list
        """
        with self.lock:
            return [{'ip': n['ip'], 'port': n['port']} for n in self.neighbors]
    
    def get_neighbor_count(self):
        """Get number of neighbors."""
        with self.lock:
            return len(self.neighbors)
    
    def clear(self):
        """Clear all neighbors."""
        with self.lock:
            self.neighbors.clear()
    
    def __str__(self):
        """String representation of routing table."""
        with self.lock:
            if not self.neighbors:
                return "Routing Table: Empty"
            
            lines = ["Routing Table:"]
            for i, neighbor in enumerate(self.neighbors, 1):
                lines.append(f"  {i}. {neighbor['ip']}:{neighbor['port']}")
            return "\n".join(lines)
