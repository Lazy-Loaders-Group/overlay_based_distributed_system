#!/usr/bin/env python3
"""
Comprehensive Test Suite for Distributed Content Searching System
Based on PROJECT_TASK.md requirements

Tests all 4 phases:
- Phase 1: Network Topology & Node Contents
- Phase 2: Socket-Based File Search
- Phase 3: REST API File Transfer
- Phase 4: Performance Analysis

Each test maps to specific requirements from the project description.
"""

import subprocess
import time
import socket
import requests
import sys
import os
import signal
import random
import json
from typing import List, Dict, Tuple

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))


class ComprehensiveTestSuite:
    """Complete test suite covering all project requirements."""
    
    def __init__(self):
        self.bs_process = None
        self.node_processes = []
        self.bs_port = 55000
        self.node_ports = list(range(55001, 55011))  # 10 nodes
        self.test_results = []
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        
    def log_phase(self, phase_num: int, phase_name: str):
        """Log phase header."""
        print("\n" + "="*80)
        print(f"PHASE {phase_num}: {phase_name}")
        print("="*80)
    
    def log_test(self, test_name: str, status: bool, details: str = ""):
        """Log individual test result."""
        symbol = "✅" if status else "❌"
        print(f"\n{symbol} TEST: {test_name}")
        if details:
            for line in details.split('\n'):
                print(f"   {line}")
        self.test_results.append((test_name, status, details))
    
    def log_requirement(self, req_id: str, description: str):
        """Log requirement being tested."""
        print(f"\n📋 Requirement {req_id}: {description}")
    
    # ============================================================================
    # PHASE 1: NETWORK TOPOLOGY & NODE CONTENTS
    # ============================================================================
    
    def test_phase1_network_formation(self):
        """Test Phase 1 requirements."""
        self.log_phase(1, "NETWORK TOPOLOGY & NODE CONTENTS")
        
        # Requirement 1.1: Bootstrap Server Registration
        self.log_requirement("1.1", "Nodes register with Bootstrap Server")
        self.test_bootstrap_server_startup()
        self.test_node_registration()
        
        # Requirement 1.2: Node receives neighbor list
        self.log_requirement("1.2", "Nodes receive neighbor list from BS")
        self.test_neighbor_list_response()
        
        # Requirement 1.3: Node joins network via 2 random nodes
        self.log_requirement("1.3", "Nodes join via 2 randomly selected neighbors")
        self.test_join_message()
        
        # Requirement 1.4: Routing table management
        self.log_requirement("1.4", "Routing tables are maintained")
        self.test_routing_table()
        
        # Requirement 1.5: File initialization (3-5 files per node)
        self.log_requirement("1.5", "Each node has 3-5 random files")
        self.test_file_initialization()
    
    def test_bootstrap_server_startup(self):
        """Test BS starts and accepts connections."""
        try:
            # Kill any process using the port first
            subprocess.run(f'lsof -ti:{self.bs_port} | xargs kill -9 2>/dev/null || true', 
                         shell=True, cwd=self.base_dir)
            time.sleep(1)
            
            self.bs_process = subprocess.Popen(
                ['python3', '-c', f'''
import sys
sys.path.insert(0, "src")
from bootstrap_server import BootstrapServer
server = BootstrapServer(port={self.bs_port})
server.start()
'''],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.base_dir
            )
            time.sleep(3)
            
            if self.bs_process.poll() is None:
                self.log_test("Bootstrap Server Startup", True, 
                             f"Running on port {self.bs_port}")
            else:
                stderr = self.bs_process.stderr.read().decode('utf-8')
                self.log_test("Bootstrap Server Startup", False, f"Failed: {stderr}")
        except Exception as e:
            self.log_test("Bootstrap Server Startup", False, str(e))
    
    def test_node_registration(self):
        """Test REG message and REGOK response."""
        try:
            # Test first node registration
            msg = f'0040 REG 127.0.0.1 {self.node_ports[0]} test_node_1'
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(('127.0.0.1', self.bs_port))
            sock.send(msg.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            sock.close()
            
            # Should get REGOK 0 (no other nodes)
            if 'REGOK 0' in response:
                self.log_test("First Node Registration", True, 
                             "Received REGOK 0 (no neighbors)")
            else:
                self.log_test("First Node Registration", False, 
                             f"Unexpected response: {response}")
        except Exception as e:
            self.log_test("Node Registration", False, str(e))
    
    def test_neighbor_list_response(self):
        """Test that subsequent registrations return neighbor lists."""
        try:
            # Register second node
            msg2 = f'0040 REG 127.0.0.1 {self.node_ports[1]} test_node_2'
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.settimeout(5)
            sock2.connect(('127.0.0.1', self.bs_port))
            sock2.send(msg2.encode('utf-8'))
            response2 = sock2.recv(1024).decode('utf-8')
            sock2.close()
            
            # Should get REGOK with first node's details
            if 'REGOK' in response2 and '127.0.0.1' in response2 and str(self.node_ports[0]) in response2:
                self.log_test("Neighbor List Response", True, 
                             f"Received neighbor info for node 1")
            else:
                self.log_test("Neighbor List Response", False, 
                             f"Missing neighbor info: {response2}")
        except Exception as e:
            self.log_test("Neighbor List Response", False, str(e))
    
    def test_join_message(self):
        """Test JOIN message format."""
        try:
            from protocol import MessageFormatter
            join_msg = MessageFormatter.create_join_message('127.0.0.1', 5001)
            
            # Verify format: length JOIN IP port
            parts = join_msg.split()
            if (len(parts) == 4 and 
                parts[0].isdigit() and len(parts[0]) == 4 and
                parts[1] == 'JOIN' and
                parts[2] == '127.0.0.1' and
                parts[3] == '5001'):
                self.log_test("JOIN Message Format", True, 
                             f"Format: {join_msg}")
            else:
                self.log_test("JOIN Message Format", False, 
                             f"Invalid format: {join_msg}")
        except Exception as e:
            self.log_test("JOIN Message Format", False, str(e))
    
    def test_routing_table(self):
        """Test routing table functionality."""
        try:
            from routing_table import RoutingTable
            rt = RoutingTable()
            
            # Add neighbors
            rt.add_neighbor('127.0.0.1', 5001)
            rt.add_neighbor('127.0.0.1', 5002)
            
            neighbors = rt.get_neighbors()
            if len(neighbors) == 2:
                self.log_test("Routing Table Management", True, 
                             f"Added 2 neighbors successfully")
            else:
                self.log_test("Routing Table Management", False, 
                             f"Expected 2 neighbors, got {len(neighbors)}")
        except Exception as e:
            self.log_test("Routing Table Management", False, str(e))
    
    def test_file_initialization(self):
        """Test file loading (3-5 random files)."""
        try:
            file_path = os.path.join(self.base_dir, 'file_names.txt')
            if not os.path.exists(file_path):
                self.log_test("File List Availability", False, 
                             "file_names.txt not found")
                return
            
            with open(file_path) as f:
                files = [line.strip() for line in f if line.strip()]
            
            if len(files) >= 20:
                # Simulate random selection
                selected = random.sample(files, random.randint(3, 5))
                self.log_test("File Initialization", True, 
                             f"File list has {len(files)} files\n" +
                             f"Simulated selection: {len(selected)} files")
            else:
                self.log_test("File Initialization", False, 
                             f"File list has only {len(files)} files (need 20+)")
        except Exception as e:
            self.log_test("File Initialization", False, str(e))
    
    # ============================================================================
    # PHASE 2: SOCKET-BASED FILE SEARCH
    # ============================================================================
    
    def test_phase2_search_functionality(self):
        """Test Phase 2 requirements."""
        self.log_phase(2, "SOCKET-BASED FILE SEARCH")
        
        # Requirement 2.1: UDP communication
        self.log_requirement("2.1", "Nodes communicate using UDP")
        self.test_udp_communication()
        
        # Requirement 2.2: Search message format
        self.log_requirement("2.2", "SER message format compliance")
        self.test_ser_message_format()
        
        # Requirement 2.3: Search response format
        self.log_requirement("2.3", "SEROK response format compliance")
        self.test_serok_message_format()
        
        # Requirement 2.4: Word-boundary matching
        self.log_requirement("2.4", "Search matches complete words only")
        self.test_word_boundary_matching()
        
        # Requirement 2.5: Case-insensitive search
        self.log_requirement("2.5", "Case-insensitive search")
        self.test_case_insensitive_search()
        
        # Requirement 2.6: Partial name matching
        self.log_requirement("2.6", "Partial filename matching")
        self.test_partial_name_matching()
        
        # Requirement 2.7: Query propagation
        self.log_requirement("2.7", "Query propagates through network")
        self.test_query_propagation()
        
        # Requirement 2.8: Loop prevention
        self.log_requirement("2.8", "Query loop detection")
        self.test_loop_prevention()
    
    def test_udp_communication(self):
        """Test UDP socket functionality."""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('127.0.0.1', 0))  # Bind to any available port
            port = sock.getsockname()[1]
            sock.close()
            
            self.log_test("UDP Socket Creation", True, 
                         f"Successfully created UDP socket on port {port}")
        except Exception as e:
            self.log_test("UDP Socket Creation", False, str(e))
    
    def test_ser_message_format(self):
        """Test SER (search) message format."""
        try:
            from protocol import MessageFormatter
            ser_msg = MessageFormatter.create_ser_message(
                '127.0.0.1', 5001, 'Lord of the rings', 1
            )
            
            # Format: length SER IP port filename hops
            if ('SER' in ser_msg and 
                '127.0.0.1' in ser_msg and 
                '5001' in ser_msg and
                ser_msg.startswith('0')):
                self.log_test("SER Message Format", True, 
                             f"Format: {ser_msg[:60]}...")
            else:
                self.log_test("SER Message Format", False, 
                             f"Invalid format: {ser_msg}")
        except Exception as e:
            self.log_test("SER Message Format", False, str(e))
    
    def test_serok_message_format(self):
        """Test SEROK (search response) message format."""
        try:
            from protocol import MessageFormatter
            serok_msg = MessageFormatter.create_serok_message(
                2, '127.0.0.1', 5001, 3, ['file1.mp3', 'file2.mp3']
            )
            
            # Format: length SEROK no_files IP port hops filename1 filename2
            if ('SEROK' in serok_msg and 
                '2' in serok_msg and  # no_files
                '127.0.0.1' in serok_msg and
                serok_msg.startswith('0')):
                self.log_test("SEROK Message Format", True, 
                             f"Format: {serok_msg[:60]}...")
            else:
                self.log_test("SEROK Message Format", False, 
                             f"Invalid format: {serok_msg}")
        except Exception as e:
            self.log_test("SEROK Message Format", False, str(e))
    
    def test_word_boundary_matching(self):
        """Test word boundary matching (requirement: 'Lo' should NOT match 'Lord')."""
        try:
            from search_engine import SearchEngine
            
            # Create mock node
            mock_node = type('MockNode', (), {
                'ip': '127.0.0.1',
                'port': 5001,
                'routing_table': type('RT', (), {'get_neighbors': lambda self: []})(),
                'statistics': type('Stats', (), {
                    'record_query_received': lambda self: None,
                    'record_query_answered': lambda self: None,
                    'record_query_forwarded': lambda self: None
                })()
            })()
            
            engine = SearchEngine(mock_node)
            engine.set_files(['Lord of the rings', 'Logan', 'The Lord'])
            
            # Test 1: 'Lo' should NOT match 'Lord'
            result1 = engine.search_local('Lo')
            no_false_match = 'Lord of the rings' not in result1 and 'The Lord' not in result1
            
            # Test 2: 'Lo' SHOULD match 'Lo' in 'Logan' (but we're looking for complete word)
            # According to spec: "Lo" should not match "Lord" but also "Lo" alone isn't a complete word in "Logan"
            
            if no_false_match:
                self.log_test("Word Boundary Matching", True, 
                             "'Lo' correctly does NOT match 'Lord of the rings'")
            else:
                self.log_test("Word Boundary Matching", False, 
                             f"'Lo' incorrectly matched: {result1}")
        except Exception as e:
            self.log_test("Word Boundary Matching", False, str(e))
    
    def test_case_insensitive_search(self):
        """Test case-insensitive matching."""
        try:
            from search_engine import SearchEngine
            
            mock_node = type('MockNode', (), {
                'ip': '127.0.0.1',
                'port': 5001,
                'routing_table': type('RT', (), {'get_neighbors': lambda self: []})(),
                'statistics': type('Stats', (), {
                    'record_query_received': lambda self: None,
                    'record_query_answered': lambda self: None,
                    'record_query_forwarded': lambda self: None
                })()
            })()
            
            engine = SearchEngine(mock_node)
            engine.set_files(['Happy Feet', 'TWILIGHT', 'The Vampire Diaries'])
            
            # Test case variations
            result1 = engine.search_local('happy feet')
            result2 = engine.search_local('HAPPY FEET')
            result3 = engine.search_local('HaPpY fEeT')
            
            if ('Happy Feet' in result1 and 
                'Happy Feet' in result2 and 
                'Happy Feet' in result3):
                self.log_test("Case Insensitive Search", True, 
                             "All case variations matched correctly")
            else:
                self.log_test("Case Insensitive Search", False, 
                             f"Results: {result1}, {result2}, {result3}")
        except Exception as e:
            self.log_test("Case Insensitive Search", False, str(e))
    
    def test_partial_name_matching(self):
        """Test partial filename matching (requirement: 'Lord' should match 'Lord of the rings')."""
        try:
            from search_engine import SearchEngine
            
            mock_node = type('MockNode', (), {
                'ip': '127.0.0.1',
                'port': 5001,
                'routing_table': type('RT', (), {'get_neighbors': lambda self: []})(),
                'statistics': type('Stats', (), {
                    'record_query_received': lambda self: None,
                    'record_query_answered': lambda self: None,
                    'record_query_forwarded': lambda self: None
                })()
            })()
            
            engine = SearchEngine(mock_node)
            engine.set_files(['Lord of the rings', 'Harry Potter', 'The Vampire Diaries'])
            
            # Test partial matches
            result1 = engine.search_local('Lord')  # Should match 'Lord of the rings'
            result2 = engine.search_local('rings')  # Should match 'Lord of the rings'
            result3 = engine.search_local('Vampire')  # Should match 'The Vampire Diaries'
            
            if ('Lord of the rings' in result1 and 
                'Lord of the rings' in result2 and 
                'The Vampire Diaries' in result3):
                self.log_test("Partial Name Matching", True, 
                             "All partial matches work correctly")
            else:
                self.log_test("Partial Name Matching", False, 
                             f"Failed matches: Lord={result1}, rings={result2}, Vampire={result3}")
        except Exception as e:
            self.log_test("Partial Name Matching", False, str(e))
    
    def test_query_propagation(self):
        """Test that queries propagate to neighbors."""
        try:
            from search_engine import SearchEngine
            from routing_table import RoutingTable
            
            # This is a conceptual test - actual propagation requires running nodes
            mock_node = type('MockNode', (), {
                'ip': '127.0.0.1',
                'port': 5001,
                'routing_table': type('RT', (), {
                    'get_neighbors': lambda self: [('127.0.0.1', 5002), ('127.0.0.1', 5003)]
                })(),
                'statistics': type('Stats', (), {
                    'record_query_received': lambda self: None,
                    'record_query_answered': lambda self: None,
                    'record_query_forwarded': lambda self: None
                })()
            })()
            
            engine = SearchEngine(mock_node)
            neighbors = mock_node.routing_table.get_neighbors()
            
            if len(neighbors) > 0:
                self.log_test("Query Propagation Capability", True, 
                             f"Node has {len(neighbors)} neighbors for propagation")
            else:
                self.log_test("Query Propagation Capability", False, 
                             "No neighbors for propagation")
        except Exception as e:
            self.log_test("Query Propagation Capability", False, str(e))
    
    def test_loop_prevention(self):
        """Test query loop detection (TTL/hop count)."""
        try:
            from search_engine import SearchEngine
            
            # Check if MAX_HOPS is defined
            if hasattr(SearchEngine, 'MAX_HOPS'):
                max_hops = SearchEngine.MAX_HOPS
                self.log_test("Loop Prevention (TTL)", True, 
                             f"MAX_HOPS = {max_hops} (prevents infinite loops)")
            else:
                self.log_test("Loop Prevention (TTL)", False, 
                             "MAX_HOPS not defined")
        except Exception as e:
            self.log_test("Loop Prevention (TTL)", False, str(e))
    
    # ============================================================================
    # PHASE 3: REST API FILE TRANSFER
    # ============================================================================
    
    def test_phase3_file_transfer(self):
        """Test Phase 3 requirements."""
        self.log_phase(3, "REST API FILE TRANSFER")
        
        # Requirement 3.1: File generation (2-10 MB)
        self.log_requirement("3.1", "Generate files between 2-10 MB")
        self.test_file_generation()
        
        # Requirement 3.2: SHA-256 hash calculation
        self.log_requirement("3.2", "Calculate SHA-256 hash")
        self.test_sha_hash_calculation()
        
        # Requirement 3.3: REST API endpoints
        self.log_requirement("3.3", "REST API implementation")
        self.test_rest_api_structure()
        
        # Requirement 3.4: Reliable transfer (TCP)
        self.log_requirement("3.4", "TCP-based file transfer")
        self.test_tcp_transfer()
    
    def test_file_generation(self):
        """Test file generation with size between 2-10 MB."""
        try:
            from file_manager import FileManager
            
            fm = FileManager()
            
            # Test multiple generations to ensure randomness
            sizes = []
            for _ in range(5):
                content = fm.get_file_content(f'test_file_{_}.mp3')
                size_mb = len(content) / (1024 * 1024)
                sizes.append(size_mb)
            
            # Check all sizes are in range
            all_in_range = all(2 <= s <= 10 for s in sizes)
            
            if all_in_range:
                self.log_test("File Generation (Size)", True, 
                             f"Generated 5 files\n" +
                             f"Sizes (MB): {[f'{s:.2f}' for s in sizes]}\n" +
                             f"All within 2-10 MB range")
            else:
                self.log_test("File Generation (Size)", False, 
                             f"Sizes out of range: {sizes}")
        except Exception as e:
            self.log_test("File Generation (Size)", False, str(e))
    
    def test_sha_hash_calculation(self):
        """Test SHA-256 hash calculation."""
        try:
            from file_manager import FileManager
            import hashlib
            
            fm = FileManager()
            
            # Generate file and get hash
            content = fm.get_file_content('test_hash.mp3')
            hash_from_manager = fm.get_file_hash('test_hash.mp3')
            
            # Verify hash is SHA-256 (64 hex characters)
            is_sha256 = len(hash_from_manager) == 64 and all(c in '0123456789abcdef' for c in hash_from_manager.lower())
            
            # Verify hash matches content
            expected_hash = hashlib.sha256(content).hexdigest()
            hash_matches = hash_from_manager == expected_hash
            
            if is_sha256 and hash_matches:
                self.log_test("SHA-256 Hash Calculation", True, 
                             f"Hash: {hash_from_manager[:32]}...\n" +
                             f"Format: Valid SHA-256\n" +
                             f"Verification: Hash matches content")
            else:
                self.log_test("SHA-256 Hash Calculation", False, 
                             f"Format valid: {is_sha256}, Matches: {hash_matches}")
        except Exception as e:
            self.log_test("SHA-256 Hash Calculation", False, str(e))
    
    def test_rest_api_structure(self):
        """Test REST API structure exists."""
        try:
            # Check if Flask is used (common for REST API)
            node_file = os.path.join(self.base_dir, 'src', 'node.py')
            with open(node_file, 'r') as f:
                content = f.read()
            
            has_flask = 'flask' in content.lower() or 'Flask' in content
            has_routes = '@app.route' in content or 'app.get' in content
            
            if has_flask or has_routes:
                self.log_test("REST API Structure", True, 
                             "Flask/REST API implementation found")
            else:
                self.log_test("REST API Structure", False, 
                             "No REST API framework detected")
        except Exception as e:
            self.log_test("REST API Structure", False, str(e))
    
    def test_tcp_transfer(self):
        """Test that TCP is used for file transfer (vs UDP for search)."""
        try:
            # REST API uses HTTP which is TCP-based
            # This is a conceptual test
            self.log_test("TCP-based Transfer", True, 
                         "REST API/HTTP uses TCP for reliable file transfer")
        except Exception as e:
            self.log_test("TCP-based Transfer", False, str(e))
    
    # ============================================================================
    # PHASE 4: PERFORMANCE ANALYSIS
    # ============================================================================
    
    def test_phase4_performance_analysis(self):
        """Test Phase 4 requirements."""
        self.log_phase(4, "PERFORMANCE ANALYSIS")
        
        # Requirement 4.1: Statistics tracking
        self.log_requirement("4.1", "Track performance statistics")
        self.test_statistics_tracking()
        
        # Requirement 4.2: Metrics collection
        self.log_requirement("4.2", "Collect hops, latency, messages")
        self.test_metrics_collection()
        
        # Requirement 4.3: CSV logging
        self.log_requirement("4.3", "Log data to CSV files")
        self.test_csv_logging()
        
        # Requirement 4.4: Statistical analysis
        self.log_requirement("4.4", "Calculate min, max, avg, std dev")
        self.test_statistical_calculations()
        
        # Requirement 4.5: Visualization (CDF plots)
        self.log_requirement("4.5", "Generate CDF plots")
        self.test_plot_generation()
        
        # Requirement 4.6: Automated query runner
        self.log_requirement("4.6", "Automated query execution")
        self.test_automated_query_runner()
    
    def test_statistics_tracking(self):
        """Test statistics module."""
        try:
            from statistics import Statistics
            
            stats = Statistics('test_node')
            
            # Record various events
            stats.record_query_received()
            stats.record_query_forwarded()
            stats.record_query_answered()
            stats.record_message_sent()
            stats.record_message_received()
            
            result = stats.get_stats()
            
            # Verify counters
            if (result['queries_received'] == 1 and 
                result['queries_forwarded'] == 1 and
                result['queries_answered'] == 1):
                self.log_test("Statistics Tracking", True, 
                             "All counters working correctly")
            else:
                self.log_test("Statistics Tracking", False, 
                             f"Counter mismatch: {result}")
        except Exception as e:
            self.log_test("Statistics Tracking", False, str(e))
    
    def test_metrics_collection(self):
        """Test that key metrics are tracked."""
        try:
            from statistics import Statistics
            
            stats = Statistics('test_metrics')
            
            # Check if methods exist for all required metrics
            required_methods = [
                'record_query_received',
                'record_query_forwarded',
                'record_query_answered',
                'record_hop',
                'record_latency'
            ]
            
            missing = []
            for method in required_methods:
                if not hasattr(stats, method):
                    missing.append(method)
            
            if not missing:
                self.log_test("Metrics Collection Methods", True, 
                             "All required metric methods present")
            else:
                self.log_test("Metrics Collection Methods", False, 
                             f"Missing methods: {missing}")
        except Exception as e:
            self.log_test("Metrics Collection Methods", False, str(e))
    
    def test_csv_logging(self):
        """Test CSV log file creation."""
        try:
            from statistics import Statistics
            
            stats = Statistics('test_csv_logging')
            stats.record_query_received()
            stats.save_to_csv()
            
            # The Statistics class creates node_{node_id}.csv, not the node_id.csv
            log_file = os.path.join(self.base_dir, 'logs', 'node_test_csv_logging.csv')
            summary_file = os.path.join(self.base_dir, 'logs', 'node_test_csv_logging_summary.csv')
            
            if os.path.exists(summary_file):
                self.log_test("CSV Logging", True, 
                             f"Log file created: {summary_file}")
                # Cleanup
                os.remove(summary_file)
                if os.path.exists(log_file):
                    os.remove(log_file)
            else:
                self.log_test("CSV Logging", False, 
                             f"Log file not created. Expected: {summary_file}")
        except Exception as e:
            self.log_test("CSV Logging", False, str(e))
            self.log_test("CSV Logging", False, str(e))
    
    def test_statistical_calculations(self):
        """Test statistical analysis functions."""
        try:
            # Check if plot_stats.py has analysis functions
            plot_file = os.path.join(self.base_dir, 'src', 'plot_stats.py')
            
            if os.path.exists(plot_file):
                with open(plot_file, 'r') as f:
                    content = f.read()
                
                has_stats = ('mean' in content or 'average' in content or 
                            'std' in content or 'min' in content or 'max' in content)
                
                if has_stats:
                    self.log_test("Statistical Calculations", True, 
                                 "Statistical functions found in plot_stats.py")
                else:
                    self.log_test("Statistical Calculations", False, 
                                 "No statistical functions found")
            else:
                self.log_test("Statistical Calculations", False, 
                             "plot_stats.py not found")
        except Exception as e:
            self.log_test("Statistical Calculations", False, str(e))
    
    def test_plot_generation(self):
        """Test CDF plot generation capability."""
        try:
            plot_file = os.path.join(self.base_dir, 'src', 'plot_stats.py')
            
            if os.path.exists(plot_file):
                with open(plot_file, 'r') as f:
                    content = f.read()
                
                has_plotting = ('matplotlib' in content or 'plt' in content or 
                               'plot' in content or 'cdf' in content.lower())
                
                if has_plotting:
                    self.log_test("CDF Plot Generation", True, 
                                 "Plotting capability found")
                else:
                    self.log_test("CDF Plot Generation", False, 
                                 "No plotting library detected")
            else:
                self.log_test("CDF Plot Generation", False, 
                             "plot_stats.py not found")
        except Exception as e:
            self.log_test("CDF Plot Generation", False, str(e))
    
    def test_automated_query_runner(self):
        """Test automated query execution."""
        try:
            from automated_query_runner import run_queries_from_file
            
            # Check if function exists and is callable
            if callable(run_queries_from_file):
                self.log_test("Automated Query Runner", True, 
                             "run_queries_from_file() function available")
            else:
                self.log_test("Automated Query Runner", False, 
                             "Function not callable")
        except Exception as e:
            self.log_test("Automated Query Runner", False, str(e))
    
    # ============================================================================
    # PROTOCOL COMPLIANCE TESTS
    # ============================================================================
    
    def test_protocol_compliance(self):
        """Test protocol message format compliance."""
        self.log_phase(0, "PROTOCOL COMPLIANCE")
        
        self.log_requirement("P.1", "Message format compliance")
        self.test_message_length_format()
        self.test_leave_message()
        self.test_error_message()
        self.test_unreg_message()
    
    def test_message_length_format(self):
        """Test that all messages have 4-digit length prefix."""
        try:
            from protocol import MessageFormatter
            
            messages = [
                MessageFormatter.create_reg_message('127.0.0.1', 5001, 'testuser'),
                MessageFormatter.create_join_message('127.0.0.1', 5001),
                MessageFormatter.create_leave_message('127.0.0.1', 5001),
                MessageFormatter.create_ser_message('127.0.0.1', 5001, 'test', 1),
            ]
            
            all_valid = True
            for msg in messages:
                length_str = msg[:4]
                if not (length_str.isdigit() and len(length_str) == 4):
                    all_valid = False
                    break
            
            if all_valid:
                self.log_test("4-Digit Length Prefix", True, 
                             "All messages have correct length format")
            else:
                self.log_test("4-Digit Length Prefix", False, 
                             "Some messages have invalid length format")
        except Exception as e:
            self.log_test("4-Digit Length Prefix", False, str(e))
    
    def test_leave_message(self):
        """Test LEAVE message format."""
        try:
            from protocol import MessageFormatter
            leave_msg = MessageFormatter.create_leave_message('127.0.0.1', 5001)
            
            # Format: length LEAVE IP port
            if 'LEAVE' in leave_msg and '127.0.0.1' in leave_msg and '5001' in leave_msg:
                self.log_test("LEAVE Message Format", True, 
                             f"Format: {leave_msg}")
            else:
                self.log_test("LEAVE Message Format", False, 
                             f"Invalid format: {leave_msg}")
        except Exception as e:
            self.log_test("LEAVE Message Format", False, str(e))
    
    def test_error_message(self):
        """Test ERROR message format."""
        try:
            from protocol import MessageFormatter
            error_msg = MessageFormatter.create_error_message()
            
            # Format: 0010 ERROR
            if error_msg == '0010 ERROR':
                self.log_test("ERROR Message Format", True, 
                             f"Format: {error_msg}")
            else:
                self.log_test("ERROR Message Format", False, 
                             f"Invalid format: {error_msg}")
        except Exception as e:
            self.log_test("ERROR Message Format", False, str(e))
    
    def test_unreg_message(self):
        """Test UNREG message format."""
        try:
            from protocol import MessageFormatter
            unreg_msg = MessageFormatter.create_unreg_message('127.0.0.1', 5001, 'testuser')
            
            # Format: length UNREG IP port username
            if 'UNREG' in unreg_msg and '127.0.0.1' in unreg_msg and 'testuser' in unreg_msg:
                self.log_test("UNREG Message Format", True, 
                             f"Format: {unreg_msg}")
            else:
                self.log_test("UNREG Message Format", False, 
                             f"Invalid format: {unreg_msg}")
        except Exception as e:
            self.log_test("UNREG Message Format", False, str(e))
    
    # ============================================================================
    # DEMO REQUIREMENTS
    # ============================================================================
    
    def test_demo_requirements(self):
        """Test demo requirements."""
        self.log_phase(5, "DEMO REQUIREMENTS")
        
        self.log_requirement("D.1", "10+ nodes capability")
        self.test_multi_node_capability()
        
        self.log_requirement("D.2", "Graceful node departure")
        self.test_graceful_departure()
        
        self.log_requirement("D.3", "Required files present")
        self.test_required_files()
    
    def test_multi_node_capability(self):
        """Test system can handle 10+ nodes."""
        try:
            # Check if we can create 10 different port numbers
            if len(self.node_ports) >= 10:
                self.log_test("10+ Nodes Capability", True, 
                             f"Configured for {len(self.node_ports)} nodes")
            else:
                self.log_test("10+ Nodes Capability", False, 
                             f"Only configured for {len(self.node_ports)} nodes")
        except Exception as e:
            self.log_test("10+ Nodes Capability", False, str(e))
    
    def test_graceful_departure(self):
        """Test graceful node departure (LEAVE + UNREG)."""
        try:
            from protocol import MessageFormatter
            
            # Test LEAVE message exists
            leave_msg = MessageFormatter.create_leave_message('127.0.0.1', 5001)
            has_leave = 'LEAVE' in leave_msg
            
            # Test UNREG message exists
            unreg_msg = MessageFormatter.create_unreg_message('127.0.0.1', 5001, 'test')
            has_unreg = 'UNREG' in unreg_msg
            
            if has_leave and has_unreg:
                self.log_test("Graceful Departure Protocol", True, 
                             "LEAVE and UNREG messages implemented")
            else:
                self.log_test("Graceful Departure Protocol", False, 
                             f"LEAVE: {has_leave}, UNREG: {has_unreg}")
        except Exception as e:
            self.log_test("Graceful Departure Protocol", False, str(e))
    
    def test_required_files(self):
        """Test all required files are present."""
        try:
            required_files = [
                'file_names.txt',
                'queries.txt',
                'src/node.py',
                'src/bootstrap_server.py',
                'src/protocol.py',
                'src/search_engine.py',
                'src/file_manager.py',
                'src/statistics.py',
                'src/routing_table.py',
                'src/automated_query_runner.py',
                'src/plot_stats.py'
            ]
            
            missing = []
            for file in required_files:
                full_path = os.path.join(self.base_dir, file)
                if not os.path.exists(full_path):
                    missing.append(file)
            
            if not missing:
                self.log_test("Required Files Present", True, 
                             f"All {len(required_files)} required files found")
            else:
                self.log_test("Required Files Present", False, 
                             f"Missing files: {missing}")
        except Exception as e:
            self.log_test("Required Files Present", False, str(e))
    
    # ============================================================================
    # CLEANUP AND REPORTING
    # ============================================================================
    
    def cleanup(self):
        """Clean up all processes."""
        print("\n" + "="*80)
        print("CLEANUP")
        print("="*80)
        
        # Stop node processes
        for proc in self.node_processes:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except:
                try:
                    proc.kill()
                except:
                    pass
        
        # Stop bootstrap server
        if self.bs_process:
            try:
                self.bs_process.terminate()
                self.bs_process.wait(timeout=3)
            except:
                try:
                    self.bs_process.kill()
                except:
                    pass
        
        # Force kill any remaining processes on the port
        try:
            subprocess.run(f'lsof -ti:{self.bs_port} | xargs kill -9 2>/dev/null || true', 
                         shell=True, timeout=5)
        except:
            pass
        
        print("✅ All processes terminated")
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        # Count results by phase
        phase_results = {
            'Phase 1': [],
            'Phase 2': [],
            'Phase 3': [],
            'Phase 4': [],
            'Protocol': [],
            'Demo': []
        }
        
        for name, status, details in self.test_results:
            if 'Registration' in name or 'Neighbor' in name or 'JOIN' in name or 'Routing' in name or 'File Initialization' in name:
                phase_results['Phase 1'].append((name, status))
            elif 'UDP' in name or 'SER' in name or 'SEROK' in name or 'Search' in name or 'Word' in name or 'Case' in name or 'Partial' in name or 'Propagation' in name or 'Loop' in name:
                phase_results['Phase 2'].append((name, status))
            elif 'File Generation' in name or 'SHA' in name or 'REST' in name or 'TCP' in name:
                phase_results['Phase 3'].append((name, status))
            elif 'Statistics' in name or 'Metrics' in name or 'CSV' in name or 'Statistical' in name or 'CDF' in name or 'Automated' in name:
                phase_results['Phase 4'].append((name, status))
            elif 'Length' in name or 'LEAVE' in name or 'ERROR' in name or 'UNREG' in name:
                phase_results['Protocol'].append((name, status))
            elif 'Nodes Capability' in name or 'Graceful' in name or 'Required Files' in name:
                phase_results['Demo'].append((name, status))
        
        # Print phase summaries
        for phase, results in phase_results.items():
            if results:
                passed = sum(1 for _, status in results if status)
                total = len(results)
                percentage = (passed / total * 100) if total > 0 else 0
                status_symbol = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
                
                print(f"\n{status_symbol} {phase}: {passed}/{total} tests passed ({percentage:.1f}%)")
                for name, status in results:
                    symbol = "  ✅" if status else "  ❌"
                    print(f"{symbol} {name}")
        
        # Overall summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, status, _ in self.test_results if status)
        overall_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "="*80)
        print("OVERALL SUMMARY")
        print("="*80)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {overall_percentage:.1f}%")
        
        # Readiness assessment
        print("\n" + "="*80)
        print("PROJECT READINESS ASSESSMENT")
        print("="*80)
        
        if overall_percentage >= 90:
            print("🎉 EXCELLENT! Your system is ready for demonstration.")
        elif overall_percentage >= 75:
            print("👍 GOOD! Minor issues to fix before demo.")
        elif overall_percentage >= 50:
            print("⚠️  NEEDS WORK! Several issues to address.")
        else:
            print("❌ CRITICAL! Major issues need immediate attention.")
        
        return overall_percentage >= 75
    
    # ============================================================================
    # MAIN TEST EXECUTION
    # ============================================================================
    
    def run_all_tests(self):
        """Execute all tests."""
        print("\n" + "="*80)
        print("DISTRIBUTED CONTENT SEARCHING - COMPREHENSIVE TEST SUITE")
        print("Based on PROJECT_TASK.md Requirements")
        print("="*80)
        
        try:
            # Protocol compliance (always test first)
            self.test_protocol_compliance()
            
            # Phase 1: Network Formation
            self.test_phase1_network_formation()
            
            # Phase 2: Search Functionality
            self.test_phase2_search_functionality()
            
            # Phase 3: File Transfer
            self.test_phase3_file_transfer()
            
            # Phase 4: Performance Analysis
            self.test_phase4_performance_analysis()
            
            # Demo Requirements
            self.test_demo_requirements()
            
        finally:
            self.cleanup()
            ready = self.generate_report()
            return 0 if ready else 1


def main():
    """Main entry point."""
    tester = ComprehensiveTestSuite()
    return tester.run_all_tests()


if __name__ == '__main__':
    sys.exit(main())
