"""
Main node implementation for distributed content searching system.
"""

import socket
import threading
import random
import sys
import argparse
import time
from protocol import MessageFormatter, MessageParser
from routing_table import RoutingTable
from search_engine import SearchEngine
from statistics import Statistics
from bootstrap_manager import BootstrapManager
from file_manager import FileManager
from flask import Flask, make_response
import requests
import logging
import io


class Node:
    """Main node class orchestrating all functionality."""
    
    def __init__(self, ip, port, username, bs_ip, bs_port):
        self.ip = ip
        self.port = port
        self.username = username
        self.bs_ip = bs_ip
        self.bs_port = bs_port
        
        # Components
        self.routing_table = RoutingTable()
        self.search_engine = SearchEngine(self)
        self.statistics = Statistics(f"{ip}_{port}")
        self.bootstrap_manager = BootstrapManager(bs_ip, bs_port, ip, port, username)
        self.file_manager = FileManager()
        
        # UDP socket
        self.sock = None
        self.running = False
        self.listener_thread = None
        
        # Files
        self.files = []
        
        print(f"[NODE] Initialized at {ip}:{port}")
    
    def load_files(self, file_list_path):
        """Load and randomly select 3-5 files."""
        try:
            with open(file_list_path, 'r') as f:
                all_files = [line.strip() for line in f if line.strip()]
            
            # Select 3-5 files randomly
            num_files = random.randint(3, 5)
            self.files = random.sample(all_files, min(num_files, len(all_files)))
            self.search_engine.set_files(self.files)
            
            print(f"[FILES] Loaded {len(self.files)} files:")
            for f in self.files:
                print(f"  - {f}")
                
        except Exception as e:
            print(f"[ERROR] Failed to load files: {e}")
    
    def start(self):
        """Start the node."""
        try:
            # Create UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.ip, self.port))
            self.running = True
            
            # Start listener thread
            self.listener_thread = threading.Thread(target=self._listen, daemon=True)
            self.listener_thread.start()
            
            # Start REST API thread
            self.rest_thread = threading.Thread(target=self._start_rest_api, daemon=True)
            self.rest_thread.start()
            
            print(f"[NODE] Started listening on {self.ip}:{self.port}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to start node: {e}")
            return False
    
    def _listen(self):
        """Listen for incoming UDP messages."""
        self.sock.settimeout(1.0)
        
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                self.statistics.record_message_received()
                
                # Process message in separate thread to avoid blocking
                threading.Thread(
                    target=self._handle_message,
                    args=(data, addr),
                    daemon=True
                ).start()
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"[ERROR] Listener error: {e}")

    def _start_rest_api(self):
        """Start Flask REST API for file transfer."""
        app = Flask(__name__)
        
        # Silence Flask logs
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        @app.route('/download/<filename>', methods=['GET'])
        def download_file(filename):
            # Check if we have this file
            if filename not in self.files:
                return "File not found", 404
                
            try:
                content = self.file_manager.get_file_content(filename)
                hash_val = self.file_manager.get_file_hash(filename)
                
                response = make_response(content)
                response.headers['Content-Type'] = 'application/octet-stream'
                response.headers['X-File-Hash'] = hash_val
                return response
            except Exception as e:
                return str(e), 500
        
        try:
            # Run Flask server
            # Note: In a real scenario, we might want to handle port conflicts if UDP and TCP ports must be different.
            # Here we assume we can bind TCP to the same port number as UDP.
            app.run(host=self.ip, port=self.port, threaded=True, debug=False, use_reloader=False)
        except Exception as e:
            print(f"[ERROR] Failed to start REST API: {e}")
    
    def _handle_message(self, data, addr):
        """Handle incoming message."""
        try:
            tokens = MessageFormatter.parse_message(data)
            if not tokens:
                return
            
            command = tokens[0]
            
            if command == 'JOIN':
                self._handle_join(tokens, addr)
            elif command == 'JOINOK':
                self._handle_joinok(tokens, addr)
            elif command == 'LEAVE':
                self._handle_leave(tokens, addr)
            elif command == 'SER':
                self._handle_search(tokens, addr)
            elif command == 'SEROK':
                self._handle_search_response(tokens, addr)
            else:
                print(f"[WARN] Unknown command: {command}")
                
        except Exception as e:
            print(f"[ERROR] Message handling error: {e}")
    
    def _handle_join(self, tokens, addr):
        """Handle JOIN message."""
        parsed = MessageParser.parse_join(tokens)
        if parsed:
            ip = parsed['ip']
            port = parsed['port']
            
            # Add to routing table
            if self.routing_table.add_neighbor(ip, port):
                print(f"[JOIN] New neighbor added: {ip}:{port}")
            
            # Send JOINOK
            response = MessageFormatter.create_joinok_message(0)
            self.sock.sendto(response.encode('utf-8'), (ip, port))
            self.statistics.record_message_sent()
    
    def _handle_joinok(self, tokens, addr):
        """Handle JOINOK response."""
        # JOINOK means the other node accepted our JOIN request
        # Add them to routing table
        ip = addr[0]
        port = addr[1]
        if self.routing_table.add_neighbor(ip, port):
            print(f"[JOINOK] Connected to neighbor: {ip}:{port}")
    
    def _handle_leave(self, tokens, addr):
        """Handle LEAVE message."""
        parsed = MessageParser.parse_leave(tokens)
        if parsed:
            ip = parsed['ip']
            port = parsed['port']
            
            # Remove from routing table
            if self.routing_table.remove_neighbor(ip, port):
                print(f"[LEAVE] Neighbor removed: {ip}:{port}")
            
            # Send LEAVEOK
            response = MessageFormatter.create_leaveok_message(0)
            self.sock.sendto(response.encode('utf-8'), (ip, port))
            self.statistics.record_message_sent()
    
    def _handle_search(self, tokens, addr):
        """Handle SER (search) message."""
        parsed = MessageParser.parse_ser(tokens)
        if parsed:
            self.search_engine.handle_search_request(
                parsed['ip'],
                parsed['port'],
                parsed['filename'],
                parsed['hops'],
                addr
            )
    
    def _handle_search_response(self, tokens, addr):
        """Handle SEROK (search response) message."""
        parsed = MessageParser.parse_serok(tokens)
        if parsed:
            self.search_engine.handle_search_response(
                parsed['num_files'],
                parsed['ip'],
                parsed['port'],
                parsed['hops'],
                parsed['filenames']
            )
    
    def register_with_bootstrap(self):
        """Register with bootstrap server and join network."""
        nodes = self.bootstrap_manager.connect_to_bs()
        
        if nodes is None:
            return False
        
        if nodes:
            # Join the network by sending JOIN to received nodes
            for node in nodes:
                self.send_join(node.ip, node.port)
            
            time.sleep(0.5)  # Give time for JOINOK responses
        
        return True
    
    def send_join(self, target_ip, target_port):
        """Send JOIN message to another node."""
        try:
            message = MessageFormatter.create_join_message(self.ip, self.port)
            self.sock.sendto(message.encode('utf-8'), (target_ip, target_port))
            self.statistics.record_message_sent()
            print(f"[JOIN] Sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"[ERROR] Failed to send JOIN: {e}")
    
    def send_leave(self, target_ip, target_port):
        """Send LEAVE message to a neighbor."""
        try:
            message = MessageFormatter.create_leave_message(self.ip, self.port)
            self.sock.sendto(message.encode('utf-8'), (target_ip, target_port))
            self.statistics.record_message_sent()
        except Exception as e:
            print(f"[ERROR] Failed to send LEAVE: {e}")
    
    def forward_search(self, target_ip, target_port, orig_ip, orig_port, filename, hops):
        """Forward search request to neighbor."""
        try:
            message = MessageFormatter.create_ser_message(orig_ip, orig_port, filename, hops)
            self.sock.sendto(message.encode('utf-8'), (target_ip, target_port))
            self.statistics.record_message_sent()
        except Exception as e:
            print(f"[ERROR] Failed to forward search: {e}")
    
    def send_search_response(self, target_ip, target_port, filenames, hops):
        """Send search response back to originator."""
        try:
            message = MessageFormatter.create_serok_message(
                len(filenames), self.ip, self.port, hops, filenames
            )
            self.sock.sendto(message.encode('utf-8'), (target_ip, target_port))
            self.statistics.record_message_sent()
        except Exception as e:
            print(f"[ERROR] Failed to send search response: {e}")
    
    def search_file(self, filename):
        """Initiate a file search."""
        print(f"\n[SEARCH] Searching for: {filename}")
        self.search_engine.initiate_search(filename)
        
    def download_file(self, ip, port, filename):
        """Download file from another node using REST API."""
        print(f"\n[DOWNLOAD] Downloading '{filename}' from {ip}:{port}...")
        try:
            url = f"http://{ip}:{port}/download/{filename}"
            start_time = time.time()
            response = requests.get(url)
            
            if response.status_code == 200:
                content = response.content
                received_hash = response.headers.get('X-File-Hash')
                
                # Calculate hash of received content
                calculated_hash = self.file_manager._calculate_hash(content)
                
                duration = time.time() - start_time
                size_mb = len(content) / (1024 * 1024)
                
                print(f"[DOWNLOAD] Success!")
                print(f"  - Size: {size_mb:.2f} MB")
                print(f"  - Time: {duration:.2f} s")
                print(f"  - Hash (Received): {received_hash}")
                print(f"  - Hash (Calculated): {calculated_hash}")
                
                if received_hash == calculated_hash:
                    print("  - Integrity Check: PASSED")
                else:
                    print("  - Integrity Check: FAILED")
            else:
                print(f"[DOWNLOAD] Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"[DOWNLOAD] Error: {e}")
    
    def leave_network(self):
        """Gracefully leave the network."""
        print("\n[LEAVE] Leaving network...")
        
        # Send LEAVE to all neighbors
        neighbors = self.routing_table.get_neighbors()
        for neighbor in neighbors:
            self.send_leave(neighbor['ip'], neighbor['port'])
        
        time.sleep(1)  # Wait for LEAVEOK responses
        
        # Unregister from bootstrap
        self.bootstrap_manager.unreg_from_bs()
        
        # Clear routing table
        self.routing_table.clear()
    
    def stop(self):
        """Stop the node."""
        self.running = False
        if self.sock:
            self.sock.close()
        self.statistics.save_summary()
        print("[NODE] Stopped")
    
    def run_cli(self):
        """Run command-line interface."""
        print("\n=== Distributed Content Search Node ===")
        print("Commands:")
        print("  register    - Register with bootstrap server")
        print("  search      - Search for a file")
        print("  run-queries - Execute all queries from queries.txt (Phase 4)")
        print("  download    - Download a file (Usage: download <ip> <port> <filename>)")
        print("  files       - Show my files")
        print("  neighbors   - Show routing table")
        print("  stats       - Show statistics")
        print("  leave       - Leave network gracefully")
        print("  exit        - Exit")
        print("=====================================\n")
        
        while self.running:
            try:
                cmd = input("> ").strip().lower()
                
                if cmd == 'register':
                    self.register_with_bootstrap()
                
                elif cmd == 'search':
                    query = input("Enter filename to search: ").strip()
                    if query:
                        self.search_file(query)
                
                elif cmd == 'run-queries':
                    query_file = input("Enter query file path (default: queries.txt): ").strip()
                    if not query_file:
                        query_file = 'queries.txt'
                    delay = input("Delay between queries in seconds (default: 2): ").strip()
                    try:
                        delay = float(delay) if delay else 2.0
                    except ValueError:
                        delay = 2.0
                    
                    # Import and run automated query runner
                    try:
                        from automated_query_runner import run_queries_from_file
                        run_queries_from_file(self, query_file, delay)
                    except ImportError:
                        print("[ERROR] automated_query_runner module not found")
                    except Exception as e:
                        print(f"[ERROR] Failed to run queries: {e}")
                
                elif cmd.startswith('download'):
                    parts = cmd.split()
                    if len(parts) >= 4:
                        ip = parts[1]
                        port = int(parts[2])
                        filename = " ".join(parts[3:])
                        self.download_file(ip, port, filename)
                    else:
                        print("Usage: download <ip> <port> <filename>")
                
                elif cmd == 'files':
                    print("\nMy files:")
                    for f in self.files:
                        print(f"  - {f}")
                
                elif cmd == 'neighbors':
                    print(f"\n{self.routing_table}")
                    print(f"Total neighbors: {self.routing_table.get_neighbor_count()}")
                
                elif cmd == 'stats':
                    self.statistics.print_stats()
                
                elif cmd == 'leave':
                    self.leave_network()
                
                elif cmd == 'exit':
                    break
                
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n[INFO] Use 'exit' command to quit properly")
            except Exception as e:
                print(f"[ERROR] Command error: {e}")
        
        self.leave_network()
        self.stop()


def main():
    parser = argparse.ArgumentParser(description='Distributed Content Search Node')
    parser.add_argument('--ip', default='127.0.0.1', help='Node IP address')
    parser.add_argument('--port', type=int, required=True, help='Node port')
    parser.add_argument('--username', required=True, help='Unique username')
    parser.add_argument('--bs-ip', default='node1.cse.mrt.ac.lk', help='Bootstrap server IP')
    parser.add_argument('--bs-port', type=int, default=5000, help='Bootstrap server port')
    parser.add_argument('--files', default='file_names.txt', help='Path to file names list')
    parser.add_argument('--auto-register', action='store_true', help='Automatically register on startup')
    
    args = parser.parse_args()
    
    # Create node
    node = Node(args.ip, args.port, args.username, args.bs_ip, args.bs_port)
    
    # Load files
    node.load_files(args.files)
    
    # Start node
    if not node.start():
        sys.exit(1)
        
    # Auto-register if requested
    if args.auto_register:
        print("[INFO] Auto-registering...")
        if node.register_with_bootstrap():
            print("[INFO] Auto-registration successful")
        else:
            print("[ERROR] Auto-registration failed")
    
    # Run CLI
    try:
        node.run_cli()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        node.leave_network()
        node.stop()


if __name__ == '__main__':
    main()
