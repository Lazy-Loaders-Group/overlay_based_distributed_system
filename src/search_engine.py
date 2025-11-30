"""
Search engine for distributed file searching with flooding algorithm.
"""

import re
import threading
import time
from datetime import datetime


class SearchEngine:
    """Handles file searching with flooding algorithm and query management."""
    
    MAX_HOPS = 10  # Maximum hops to prevent excessive forwarding
    
    def __init__(self, node):
        self.node = node
        self.files = []
        self.query_cache = set()  # Track seen queries to avoid loops
        self.cache_lock = threading.Lock()
        self.pending_queries = {}  # Track queries waiting for responses
        self.pending_lock = threading.Lock()
    
    def set_files(self, files):
        """Set the list of files this node has."""
        self.files = files
    
    def search_local(self, query):
        """
        Search for files locally using word-boundary matching.
        
        Args:
            query (str): Search query
            
        Returns:
            list: Matching filenames
        """
        query_words = query.lower().split()
        matches = []
        
        for filename in self.files:
            filename_lower = filename.lower()
            # Check if all query words appear as complete words in filename
            all_match = True
            for word in query_words:
                # Use word boundary regex for exact word matching
                pattern = r'\b' + re.escape(word) + r'\b'
                if not re.search(pattern, filename_lower):
                    all_match = False
                    break
            
            if all_match:
                matches.append(filename)
        
        return matches
    
    def generate_query_id(self, originator_ip, originator_port):
        """Generate unique query ID."""
        timestamp = int(time.time() * 1000)
        return f"{originator_ip}:{originator_port}:{timestamp}"
    
    def is_query_seen(self, query_id):
        """Check if query has been seen before."""
        with self.cache_lock:
            return query_id in self.query_cache
    
    def mark_query_seen(self, query_id):
        """Mark query as seen."""
        with self.cache_lock:
            self.query_cache.add(query_id)
    
    def handle_search_request(self, originator_ip, originator_port, filename, hops, sender_addr):
        """
        Handle incoming search request.
        
        Args:
            originator_ip (str): IP of node that initiated search
            originator_port (int): Port of node that initiated search
            filename (str): File to search for
            hops (int): Number of hops so far
            sender_addr (tuple): (ip, port) of node that sent this message
        """
        # Check TTL - drop if exceeded max hops
        if hops >= self.MAX_HOPS:
            return
        
        # Generate query ID
        query_id = self.generate_query_id(originator_ip, originator_port)
        
        # Check if already processed
        if self.is_query_seen(query_id):
            return
        
        # Mark as seen
        self.mark_query_seen(query_id)
        
        # Search locally
        matches = self.search_local(filename)
        
        # Log the search
        self.node.statistics.record_query_received()
        
        if matches:
            # Found files - send response back to originator
            self.node.statistics.record_query_answered()
            self.node.send_search_response(
                originator_ip, originator_port, matches, hops
            )
            print(f"[SEARCH] Found {len(matches)} file(s) for '{filename}': {matches}")
        
        # Forward to neighbors (flooding) - except sender
        neighbors = self.node.routing_table.get_neighbors()
        forwarded = False
        
        for neighbor in neighbors:
            # Don't send back to sender
            if neighbor['ip'] == sender_addr[0] and neighbor['port'] == sender_addr[1]:
                continue
            
            # Don't send back to originator
            if neighbor['ip'] == originator_ip and neighbor['port'] == originator_port:
                continue
            
            # Forward the search with incremented hop count
            self.node.forward_search(
                neighbor['ip'], neighbor['port'],
                originator_ip, originator_port,
                filename, hops + 1
            )
            forwarded = True
        
        if forwarded:
            self.node.statistics.record_query_forwarded()
    
    def initiate_search(self, filename):
        """
        Initiate a new search from this node.
        
        Args:
            filename (str): File to search for
            
        Returns:
            str: Query ID for tracking
        """
        query_id = self.generate_query_id(self.node.ip, self.node.port)
        self.mark_query_seen(query_id)
        
        # Store pending query info
        with self.pending_lock:
            self.pending_queries[query_id] = {
                'filename': filename,
                'start_time': time.time(),
                'responses': []
            }
        
        # Search locally first
        local_matches = self.search_local(filename)
        if local_matches:
            print(f"[SEARCH] Found locally: {local_matches}")
            with self.pending_lock:
                self.pending_queries[query_id]['responses'].append({
                    'ip': self.node.ip,
                    'port': self.node.port,
                    'files': local_matches,
                    'hops': 0
                })
        
        # Forward to all neighbors
        neighbors = self.node.routing_table.get_neighbors()
        if neighbors:
            for neighbor in neighbors:
                self.node.forward_search(
                    neighbor['ip'], neighbor['port'],
                    self.node.ip, self.node.port,
                    filename, 1
                )
            print(f"[SEARCH] Query forwarded to {len(neighbors)} neighbor(s)")
        else:
            print("[SEARCH] No neighbors to forward query to")
        
        return query_id
    
    def handle_search_response(self, num_files, ip, port, hops, filenames):
        """Handle incoming search response."""
        if num_files > 0:
            # Calculate latency
            latency = 0
            matched_query = None
            
            with self.pending_lock:
                # Find matching query
                # We assume the response corresponds to one of the pending queries
                # Since we don't have query ID in the protocol, and parallel queries are not required,
                # we can match with the active pending query.
                current_time = time.time()
                # Get the most recent query if multiple exist
                if self.pending_queries:
                    # Get the last added query (assuming dict preserves insertion order in Python 3.7+)
                    qid = list(self.pending_queries.keys())[-1]
                    matched_query = self.pending_queries[qid]
                    latency = (current_time - matched_query['start_time']) * 1000  # ms
            
            print(f"\n[RESULT] Found {num_files} file(s) at {ip}:{port} (hops: {hops}, latency: {latency:.2f}ms)")
            for filename in filenames:
                print(f"  - {filename}")
                
            # Log stats
            self.node.statistics.log_event(
                event_type='SEARCH_RESULT',
                query=matched_query['filename'] if matched_query else 'unknown',
                hops=hops,
                latency_ms=latency,
                sender_ip=ip,
                sender_port=port
            )
