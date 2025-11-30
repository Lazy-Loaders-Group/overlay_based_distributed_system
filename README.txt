Distributed Content Searching System
====================================

Project: Overlay-Based Distributed File Searching
Team: Lazy-Loaders-Group
Due Date: July 31, 2025

PREREQUISITES
-------------
- Python 3.8 or higher
- Network connectivity to bootstrap server: node1.cse.mrt.ac.lk:5000

INSTALLATION
------------
1. Install required packages:
   pip install -r requirements.txt

2. Ensure file_names.txt and queries.txt are in the project root

PROJECT STRUCTURE
-----------------
src/
  ├── node.py              - Main node implementation
  ├── protocol.py          - Message formatting and parsing
  ├── routing_table.py     - Neighbor management
  ├── search_engine.py     - File search with flooding
  ├── statistics.py        - Performance metrics tracking
  └── bootstrap_client.py  - Bootstrap server communication

logs/                      - Statistics logs (auto-created)
file_names.txt            - List of shareable files
queries.txt               - Test queries

RUNNING A NODE
--------------
Basic usage:
  python src/node.py --port 5001 --username myuser_node1

Full options:
  python src/node.py --ip 127.0.0.1 --port 5001 --username myuser_node1 \
                     --bs-ip node1.cse.mrt.ac.lk --bs-port 5000 \
                     --files file_names.txt

NODE COMMANDS
-------------
Once node is running, available commands:

  register    - Register with bootstrap server and join network
  search      - Search for a file in the network
  files       - Display files this node has
  neighbors   - Show routing table (connected neighbors)
  stats       - Display statistics (queries, messages, etc.)
  leave       - Gracefully leave the network
  exit        - Exit the program

TESTING LOCALLY
---------------
To run multiple nodes on same machine:

Terminal 1:
  python src/node.py --port 5001 --username test_node1

Terminal 2:
  python src/node.py --port 5002 --username test_node2

Terminal 3:
  python src/node.py --port 5003 --username test_node3

In each terminal:
1. Type 'register' to join network
2. Type 'search' to search for files
3. Use 'neighbors' to verify connections

DISTRIBUTED DEPLOYMENT
----------------------
For demo across multiple machines:

Machine 1 (IP: 192.168.1.10):
  python src/node.py --ip 192.168.1.10 --port 5001 --username team_node1

Machine 2 (IP: 192.168.1.11):
  python src/node.py --ip 192.168.1.11 --port 5001 --username team_node2

Machine 3 (IP: 192.168.1.12):
  python src/node.py --ip 192.168.1.12 --port 5001 --username team_node3

Note: Ensure firewall allows UDP traffic on chosen ports

TROUBLESHOOTING
---------------
1. "Address already in use" error:
   - Change port number or kill existing process:
     lsof -i :5001
     kill -9 <PID>

2. "Connection refused" to bootstrap server:
   - Check network connectivity
   - Verify bootstrap server is accessible:
     nc -u node1.cse.mrt.ac.lk 5000

3. "Already registered" (9998 error):
   - Unregister first using netcat:
     nc -u node1.cse.mrt.ac.lk 5000
     0040 UNREG <your-ip> <your-port> <username>

4. No search results:
   - Verify neighbors are connected: type 'neighbors'
   - Check if file exists in network: type 'files' on other nodes
   - Ensure nodes are registered: type 'register' on each

PHASE 2 COMPLETION STATUS
--------------------------
✅ Phase 1: Network topology and node registration
✅ Phase 2: UDP-based file search with flooding
⏳ Phase 3: REST API file transfer (in progress)
⏳ Phase 4: Performance analysis (in progress)

IMPLEMENTED FEATURES
--------------------
✅ Bootstrap server registration/unregistration
✅ UDP socket communication
✅ JOIN/LEAVE protocol messages
✅ Routing table management
✅ File search with word-boundary matching
✅ Flooding algorithm with loop prevention
✅ Search result routing
✅ Statistics tracking and logging
✅ Graceful node departure
✅ CLI interface

NEXT STEPS
----------
1. Implement Phase 3: REST API for file transfer
2. Add file download functionality
3. Create automation scripts for experiments
4. Develop analysis tools for Phase 4

CONTACT
-------
For questions or issues, contact team members or instructor.
