# Distributed Content Searching System - Implementation Guide

## Project Overview

**Project Name:** Overlay-Based Distributed Content Searching System  
**Due Date:** July 31, 2025  
**Team Size:** 5 members  
**Minimum Nodes:** 10+  
**Files Shared:** 20 files (3-5 files per node)

---

## Table of Contents

1. [Phase 1: Network Topology & Content Generation](#phase-1-network-topology--content-generation)
2. [Phase 2: Socket-Based File Search](#phase-2-socket-based-file-search)
3. [Phase 3: File Transfer Implementation](#phase-3-file-transfer-implementation)
4. [Phase 4: Performance Analysis](#phase-4-performance-analysis)
5. [Implementation Best Practices](#implementation-best-practices)
6. [Testing & Debugging](#testing--debugging)
7. [Deliverables & Deadlines](#deliverables--deadlines)

---

## Phase 1: Network Topology & Content Generation

### Objective
Build the network overlay structure and initialize each node with random files.

### Step 1.1: Design Document Preparation
**Timeline:** Week 1-2

#### Tasks:
- [ ] **1.1.1** Define network topology structure
  - Decide on overlay topology (unstructured/structured)
  - Each node connects to 2 randomly selected nodes
  - Design routing table format
  
- [ ] **1.1.2** Design communication protocol
  - UDP-based messaging for node discovery and search
  - Follow protocol specifications in Section 4
  - Plan message handling and error recovery
  
- [ ] **1.1.3** Create layered architecture design
  ```
  Layer 1: Network Layer (UDP Socket Communication)
  Layer 2: Protocol Layer (Message Parsing/Formatting)
  Layer 3: Application Layer (File Management, Search Logic)
  Layer 4: User Interface Layer (CLI/GUI)
  ```

- [ ] **1.1.4** Design routing table structure
  ```
  Routing Table Entry:
  - IP Address
  - Port Number
  - Status (Active/Inactive)
  - Last Active Timestamp
  ```

- [ ] **1.1.5** Define file storage format
  ```
  Node File Storage:
  - File names list (3-5 files per node)
  - File metadata (size, hash, etc.)
  ```

- [ ] **1.1.6** Create pseudo-code for core operations
  - Node registration
  - Network joining
  - File searching
  - Node leaving

- [ ] **1.1.7** Get design approval from instructor

### Step 1.2: Bootstrap Server Integration
**Timeline:** Week 2

#### Tasks:
- [ ] **1.2.1** Understand Bootstrap Server (BS) protocol
  - BS Address: `node1.cse.mrt.ac.lk:5000`
  - Test connection using netcat: `nc -u node1.cse.mrt.ac.lk 5000`
  
- [ ] **1.2.2** Implement REG (Register) message
  ```
  Format: length REG IP_address port_no username
  Example: 0036 REG 129.82.123.45 5001 1234abcd
  ```
  - Calculate message length (always 4 digits)
  - Include your IP, port, and unique username
  
- [ ] **1.2.3** Handle REGOK response
  ```
  Format: length REGOK no_nodes IP_1 port_1 IP_2 port_2 ...
  ```
  - Parse response codes:
    - 0: Success, no nodes
    - 1-2: Success with node contacts
    - 9999: Command error
    - 9998: Already registered
    - 9997: IP/port taken
    - 9996: BS full
  
- [ ] **1.2.4** Implement UNREG (Unregister) message
  ```
  Format: length UNREG IP_address port_no username
  Example: 0028 UNREG 64.12.123.190 432
  ```
  
- [ ] **1.2.5** Handle UNROK response
  - 0: Success
  - 9999: Error

### Step 1.3: Node Implementation
**Timeline:** Week 3-4

#### Tasks:
- [ ] **1.3.1** Create Node class/structure
  ```python
  class Node:
      - node_id
      - ip_address
      - port_number
      - username
      - routing_table[]
      - file_list[]
      - udp_socket
      - running_status
  ```

- [ ] **1.3.2** Implement UDP socket creation
  - Bind to specified IP and port
  - Set socket timeout for error handling
  - Handle socket exceptions

- [ ] **1.3.3** Implement file initialization
  - Read file names from `file_names.txt`
  - Randomly select 3-5 files per node
  - Store file list in node structure
  - Display selected files on startup

- [ ] **1.3.4** Implement node registration flow
  1. Create UDP socket
  2. Send REG message to BS
  3. Receive and parse REGOK
  4. Store received node contacts

- [ ] **1.3.5** Implement JOIN message handling
  ```
  Format: length JOIN IP_address port_no
  Example: 0027 JOIN 64.12.123.190 432
  ```
  - Send JOIN to 2 randomly selected nodes (from 4th node onwards)
  - Update local routing table
  - Send JOINOK response

- [ ] **1.3.6** Implement routing table management
  - Add new neighbors
  - Display routing table on demand
  - Remove inactive nodes
  - Handle routing table updates

### Step 1.4: Testing Phase 1
**Timeline:** Week 4

#### Tasks:
- [ ] **1.4.1** Test single node registration
  - Verify BS communication
  - Check REGOK response
  
- [ ] **1.4.2** Test multiple nodes (minimum 10)
  - Register all nodes sequentially
  - Verify routing tables
  - Check network topology formation
  
- [ ] **1.4.3** Test file initialization
  - Verify random file selection
  - Ensure 3-5 files per node
  - Check for file distribution across nodes
  
- [ ] **1.4.4** Test node commands
  - Display routing table command
  - Display file list command
  - Unregister command

---

## Phase 2: Socket-Based File Search

### Objective
Implement distributed file search using UDP-based message passing.

### Step 2.1: Search Protocol Implementation
**Timeline:** Week 5-6

#### Tasks:
- [ ] **2.1.1** Implement SER (Search) message
  ```
  Format: length SER IP port file_name hops
  Example: 0047 SER 129.82.62.142 5070 "Lord of the rings" 0
  ```
  - Include originating node's IP and port
  - Initialize hop count to 0
  - Support full and partial file name matching

- [ ] **2.1.2** Implement file matching logic
  - Match complete words only
  - Case-insensitive matching
  - Examples:
    - "Lord" matches "Lord of the rings"
    - "Lord rings" matches "Lord of the rings"
    - "Lo" does NOT match "Lord of the rings"

- [ ] **2.1.3** Implement SEROK (Search Response) message
  ```
  Format: length SEROK no_files IP port hops filename1 filename2 ...
  Example: 0114 SEROK 3 129.82.128.1 2301 0 baby_go_home.mp3 baby.mpeg
  ```
  - Return matching files
  - Include node IP and port
  - Include hop count
  
- [ ] **2.1.4** Handle search response codes
  - ≥1: Success with results
  - 0: No matching files
  - 9999: Node unreachable
  - 9998: Other error

### Step 2.2: Search Strategy Implementation
**Timeline:** Week 6-7

#### Tasks:
- [ ] **2.2.1** Choose search strategy
  - **Option A:** Flooding (broadcast to all neighbors)
  - **Option B:** Random walk
  - **Option C:** Intelligent routing
  - Document your choice and reasoning

- [ ] **2.2.2** Implement query forwarding
  - Forward to neighbors in routing table
  - Increment hop count
  - Avoid query loops (track query IDs)
  
- [ ] **2.2.3** Implement query ID tracking
  ```
  Query ID = originating_IP + originating_port + timestamp
  ```
  - Maintain list of processed queries
  - Drop duplicate queries
  
- [ ] **2.2.4** Implement TTL (Time To Live) mechanism
  - Set maximum hop count (e.g., 10 hops)
  - Drop queries exceeding TTL
  - Prevent infinite forwarding

- [ ] **2.2.5** Implement response routing
  - Route SEROK back to originating node
  - Use stored originating IP and port
  - Handle multiple responses

### Step 2.3: Message Statistics Tracking
**Timeline:** Week 7

#### Tasks:
- [ ] **2.3.1** Implement message counters per node
  ```python
  class Statistics:
      - queries_received
      - queries_forwarded
      - queries_answered
      - messages_sent
      - messages_received
  ```

- [ ] **2.3.2** Implement latency measurement
  - Record query start time
  - Record response received time
  - Calculate latency = response_time - query_time

- [ ] **2.3.3** Implement hop count tracking
  - Track hops in SER message
  - Report in SEROK message
  - Log for analysis

- [ ] **2.3.4** Implement logging system
  - Log all messages sent/received
  - Log timestamps
  - Log statistics per query
  - Save to file for later analysis

### Step 2.4: Node Failure Handling
**Timeline:** Week 7-8

#### Tasks:
- [ ] **2.4.1** Implement LEAVE message
  ```
  Format: length LEAVE IP_address port_no
  Example: 0028 LEAVE 64.12.123.190 432
  ```
  
- [ ] **2.4.2** Implement graceful node departure
  1. Send LEAVE to all nodes in routing table
  2. Wait for LEAVEOK responses
  3. Send UNREG to BS
  4. Close socket and exit

- [ ] **2.4.3** Handle LEAVE message reception
  - Remove leaving node from routing table
  - Send LEAVEOK response
  - Update internal state

- [ ] **2.4.4** Implement timeout mechanism
  - Detect unresponsive nodes
  - Remove from routing table after timeout
  - Continue operation with remaining nodes

### Step 2.5: Testing Phase 2
**Timeline:** Week 8

#### Tasks:
- [ ] **2.5.1** Test with provided queries
  - Use queries from `queries.txt`
  - Execute from 3 randomly selected nodes
  - Verify search results

- [ ] **2.5.2** Test partial name matching
  - Search "Lord" → should find "Lord of the rings"
  - Search "Happy" → should find "Happy Feet"
  - Verify word boundary matching

- [ ] **2.5.3** Test non-existent files
  - Query for files not in system
  - Verify proper "no results" response
  
- [ ] **2.5.4** Test node removal
  - Remove 2 random nodes gracefully
  - Verify system continues to operate
  - Repeat search tests

- [ ] **2.5.5** Collect Phase 2 statistics
  - Number of hops per query
  - Latency per query
  - Messages per node
  - Routing table sizes

---

## Phase 3: File Transfer Implementation

### Objective
Implement reliable file transfer using Web Services or REST API.

### Step 3.1: Technology Selection
**Timeline:** Week 9

#### Tasks:
- [ ] **3.1.1** Choose transfer technology
  - **Option A:** REST API (recommended if unfamiliar)
    - Use Flask/FastAPI (Python)
    - Use Express.js (Node.js)
    - Use Spring Boot (Java)
  - **Option B:** SOAP Web Services
    - Use JAX-WS (Java)
    - Use gSOAP (C++)

- [ ] **3.1.2** Design file transfer protocol
  - TCP-based for reliability
  - HTTP/HTTPS for REST API
  - Define endpoints/operations
  
- [ ] **3.1.3** Update design document
  - Add file transfer architecture
  - Document API endpoints
  - Update system diagram

### Step 3.2: REST API Implementation (Recommended)
**Timeline:** Week 9-10

#### Tasks:
- [ ] **3.2.1** Set up REST API server on each node
  ```python
  # Example endpoints
  GET  /files              → List available files
  GET  /files/{filename}   → Download specific file
  POST /files              → Upload file (optional)
  GET  /health             → Health check
  ```

- [ ] **3.2.2** Implement file generation
  ```python
  def generate_file(filename):
      # Generate random size between 2-10 MB
      size_mb = random.randint(2, 10)
      size_bytes = size_mb * 1024 * 1024
      
      # Generate random data
      data = os.urandom(size_bytes)
      
      # Calculate SHA-256 hash
      hash_value = hashlib.sha256(data).hexdigest()
      
      # Display on console
      print(f"File: {filename}")
      print(f"Size: {size_mb} MB")
      print(f"SHA-256: {hash_value}")
      
      return data, hash_value
  ```

- [ ] **3.2.3** Implement download endpoint
  - Generate file data on-demand
  - Calculate and return SHA hash
  - Stream file data to client
  - Handle errors gracefully

- [ ] **3.2.4** Implement client-side download
  ```python
  def download_file(node_ip, node_port, filename):
      url = f"http://{node_ip}:{node_port}/files/{filename}"
      response = requests.get(url, stream=True)
      
      # Download file
      with open(filename, 'wb') as f:
          for chunk in response.iter_content(chunk_size=8192):
              f.write(chunk)
      
      # Calculate hash for verification
      hash_value = calculate_hash(filename)
      return hash_value
  ```

- [ ] **3.2.5** Implement hash verification
  - Compare sender's hash with receiver's hash
  - Report verification status
  - Retry on mismatch (optional)

### Step 3.3: Integration with Phase 2
**Timeline:** Week 10

#### Tasks:
- [ ] **3.3.1** Update search response handling
  - After receiving SEROK, prompt user to download
  - Extract node IP and port from response
  - Initiate REST API download

- [ ] **3.3.2** Implement download workflow
  1. User searches for file (Phase 2)
  2. System returns node with file (SEROK)
  3. User initiates download
  4. System downloads via REST API (Phase 3)
  5. System verifies hash
  6. Display success/failure

- [ ] **3.3.3** Update CLI/GUI
  - Add download command
  - Display download progress
  - Show file size and hash
  - Report transfer time

- [ ] **3.3.4** Handle concurrent downloads
  - Support multiple simultaneous downloads
  - Manage bandwidth (optional)
  - Update UI with progress

### Step 3.4: Testing Phase 3
**Timeline:** Week 11

#### Tasks:
- [ ] **3.4.1** Test file generation
  - Verify random size (2-10 MB)
  - Verify data generation
  - Verify SHA hash calculation

- [ ] **3.4.2** Test single file download
  - Search for file
  - Download from found node
  - Verify hash matches

- [ ] **3.4.3** Test multiple downloads
  - Download same file from different nodes
  - Download different files
  - Verify all hashes

- [ ] **3.4.4** Test error handling
  - Node offline during download
  - Network interruption
  - Invalid file request

- [ ] **3.4.5** Measure transfer performance
  - Download time vs file size
  - Network throughput
  - Success rate

---

## Phase 4: Performance Analysis

### Objective
Analyze and compare performance of Phase 2 and Phase 3 implementations.

### Step 4.1: Data Collection Setup
**Timeline:** Week 12

#### Tasks:
- [ ] **4.1.1** Set up 10+ nodes
  - Deploy on different machines/ports
  - Verify all nodes registered
  - Verify routing tables populated

- [ ] **4.1.2** Select 3 random query nodes
  - Use random selection algorithm
  - Document selected nodes
  - Verify nodes are active

- [ ] **4.1.3** Prepare query execution script
  ```python
  def execute_queries(node, query_list):
      results = []
      for query in query_list:
          start_time = time.time()
          response = node.search(query)
          end_time = time.time()
          
          result = {
              'query': query,
              'hops': response.hops,
              'latency': end_time - start_time,
              'found': response.success,
              'results': response.files
          }
          results.append(result)
      return results
  ```

### Step 4.2: Experiment 1 - Full Network
**Timeline:** Week 12

#### Tasks:
- [ ] **4.2.1** Execute all queries from `queries.txt`
  - Run from 3 selected nodes
  - Execute one query at a time (sequential)
  - Log all metrics

- [ ] **4.2.2** Collect per-query metrics
  - Number of hops
  - Latency (milliseconds)
  - Success/failure
  - Response time

- [ ] **4.2.3** Collect per-node metrics
  - Queries received
  - Queries forwarded
  - Queries answered
  - Routing table size
  - Node degree (number of neighbors)

- [ ] **4.2.4** Test file downloads (Phase 3)
  - Download found files
  - Measure transfer time
  - Verify hashes
  - Record success rate

### Step 4.3: Experiment 2 - Reduced Network
**Timeline:** Week 12-13

#### Tasks:
- [ ] **4.3.1** Remove 2 random nodes
  - Select 2 nodes randomly
  - Execute graceful departure (LEAVE message)
  - Verify UNREG with BS
  - Wait for routing table updates

- [ ] **4.3.2** Repeat query execution
  - Run same queries from `queries.txt`
  - Use same 3 nodes (if still active)
  - Collect same metrics as Experiment 1

- [ ] **4.3.3** Compare with Experiment 1
  - Changes in hop count
  - Changes in latency
  - Changes in success rate
  - Impact on routing tables

### Step 4.4: Statistical Analysis
**Timeline:** Week 13

#### Tasks:
- [ ] **4.4.1** Calculate basic statistics
  - **For hops:** min, max, average, standard deviation
  - **For latency:** min, max, average, standard deviation
  - **For messages per node:** min, max, average, std dev
  - **For node degree:** min, max, average, std dev

- [ ] **4.4.2** Calculate cost metrics
  ```python
  # Per-query cost
  per_query_cost = total_messages / total_queries
  
  # Per-node cost
  per_node_cost = total_messages / number_of_nodes
  ```

- [ ] **4.4.3** Create CDF plots
  - CDF of hops distribution
  - CDF of latency distribution
  - CDF of messages per node
  - CDF of node degree
  
  ```python
  import matplotlib.pyplot as plt
  import numpy as np
  
  def plot_cdf(data, xlabel, title):
      sorted_data = np.sort(data)
      y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
      plt.plot(sorted_data, y)
      plt.xlabel(xlabel)
      plt.ylabel('CDF')
      plt.title(title)
      plt.grid(True)
      plt.show()
  ```

- [ ] **4.4.4** Create comparison tables
  - Experiment 1 vs Experiment 2
  - Phase 2 vs Phase 3 performance
  - Network topology impact

### Step 4.5: Critical Evaluation
**Timeline:** Week 13-14

#### Tasks:
- [ ] **4.5.1** Analyze scalability
  - **Scenario 1:** Q >> N (Many queries, few nodes)
    - Expected behavior
    - Bottlenecks
    - Improvement strategies
  
  - **Scenario 2:** N >> Q (Many nodes, few queries)
    - Expected behavior
    - Overhead concerns
    - Optimization opportunities

- [ ] **4.5.2** Identify bottlenecks
  - Network congestion points
  - Message overhead
  - Search inefficiencies
  - Routing limitations

- [ ] **4.5.3** Propose improvements
  - **Reduce hops:** Intelligent routing, caching
  - **Reduce latency:** Parallel queries, better topology
  - **Reduce messages:** Query aggregation, selective forwarding
  - **Improve success rate:** Better search algorithms

- [ ] **4.5.4** Compare topologies
  - Unstructured vs structured overlays
  - Random vs optimized connections
  - Flat vs hierarchical designs

### Step 4.6: Report Writing
**Timeline:** Week 14

#### Tasks:
- [ ] **4.6.1** Write methodology section
  - Experimental setup
  - Metrics collected
  - Tools used

- [ ] **4.6.2** Write results section
  - Present statistics tables
  - Include all CDF plots
  - Show comparison charts

- [ ] **4.6.3** Write discussion section
  - Interpret results
  - Explain trends
  - Compare with expectations

- [ ] **4.6.4** Write conclusion
  - Summary of findings
  - Limitations
  - Future work

- [ ] **4.6.5** Format report (max 5 pages)
  - Professional formatting
  - Clear figures and tables
  - Proper citations

---

## Implementation Best Practices

### Code Organization

```
project/
├── src/
│   ├── node.py/java/js          # Main node implementation
│   ├── protocol.py               # Message formatting/parsing
│   ├── search.py                 # Search logic
│   ├── file_transfer.py          # REST API/Web service
│   ├── statistics.py             # Metrics tracking
│   └── utils.py                  # Helper functions
├── config/
│   ├── config.json               # Configuration file
│   └── file_names.txt            # File names list
├── logs/
│   └── node_*.log                # Log files per node
├── tests/
│   ├── test_protocol.py          # Unit tests
│   ├── test_search.py
│   └── test_file_transfer.py
├── docs/
│   ├── design.md                 # Design document
│   ├── report.md                 # Performance report
│   └── reflection.md             # Personal reflection
├── README.md                     # Setup instructions
├── requirements.txt              # Dependencies
└── Makefile                      # Build instructions
```

### Error Handling

```python
# Always wrap network operations in try-catch
try:
    socket.sendto(message, (ip, port))
except socket.timeout:
    logger.error(f"Timeout sending to {ip}:{port}")
except socket.error as e:
    logger.error(f"Socket error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    filename=f'logs/node_{port}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log important events
logger.info(f"Node registered: {ip}:{port}")
logger.debug(f"Query received: {query_id}")
logger.warning(f"Node unreachable: {target_ip}")
logger.error(f"Failed to process message: {error}")
```

### Configuration Management

```json
{
  "bootstrap_server": {
    "ip": "node1.cse.mrt.ac.lk",
    "port": 5000
  },
  "node": {
    "ip": "192.168.1.100",
    "port": 5001,
    "username": "team_abc_01"
  },
  "search": {
    "max_hops": 10,
    "timeout": 5,
    "retry_count": 3
  },
  "file_transfer": {
    "api_port": 8080,
    "max_file_size_mb": 10,
    "min_file_size_mb": 2
  }
}
```

### Thread Safety

```python
import threading

class Node:
    def __init__(self):
        self.routing_table_lock = threading.Lock()
        self.statistics_lock = threading.Lock()
    
    def update_routing_table(self, entry):
        with self.routing_table_lock:
            self.routing_table.append(entry)
    
    def increment_counter(self):
        with self.statistics_lock:
            self.message_count += 1
```

### Testing Strategy

- [ ] **Unit Tests:** Test individual components (message parsing, file matching)
- [ ] **Integration Tests:** Test component interactions (search + routing)
- [ ] **System Tests:** Test full system with multiple nodes
- [ ] **Stress Tests:** Test with high query load
- [ ] **Failure Tests:** Test node failures and recovery

---

## Testing & Debugging

### Local Testing Setup

```bash
# Terminal 1 - Start first node
python node.py --port 5001 --username team_node1

# Terminal 2 - Start second node
python node.py --port 5002 --username team_node2

# Terminal 3 - Start third node
python node.py --port 5003 --username team_node3

# Continue for 10+ nodes...
```

### Testing with Bootstrap Server

```bash
# Test BS connection
nc -u node1.cse.mrt.ac.lk 5000

# Register node
0036 REG 192.168.1.100 5001 testuser

# Unregister node
0038 UNREG 192.168.1.100 5001 testuser

# Check BS status
PRINT
```

### Debugging Checklist

- [ ] Messages are properly formatted (length in 4 digits)
- [ ] UDP sockets are bound correctly
- [ ] Routing tables are updated correctly
- [ ] Query IDs prevent loops
- [ ] Timeouts are handled properly
- [ ] Errors are logged for analysis
- [ ] All threads are synchronized
- [ ] Memory leaks are prevented
- [ ] File hashes match after transfer

### Common Issues & Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| BS returns 9998 | Already registered | Send UNREG first |
| No response from node | Firewall blocking | Check firewall rules |
| Query loops | No loop prevention | Implement query ID tracking |
| File not found | Matching logic error | Review word boundary matching |
| Download fails | REST API not running | Verify API server started |
| Hash mismatch | Data corruption | Implement retry mechanism |

---

## Deliverables & Deadlines

### Deadline 1: Design Document
**Maximum:** 3 pages

**Contents:**
- [ ] Network topology diagram
- [ ] Communication protocol design
- [ ] Routing table structure
- [ ] Search strategy
- [ ] File transfer mechanism
- [ ] Performance metrics definition
- [ ] Pseudo-code for key algorithms

**Format:** PDF, properly formatted with diagrams

---

### Deadline 2: Phase 2 Implementation
**Submission:** Code + README + Makefile

**Contents:**
- [ ] Complete Phase 1 & 2 implementation
- [ ] Source code (no executables)
- [ ] README.txt with:
  - Compilation instructions
  - How to run nodes
  - Configuration parameters
  - Dependencies
- [ ] Makefile (if applicable)
- [ ] Test scripts

**Format:** .zip or .tar.gz

---

### Deadline 3: Phase 3 Implementation
**Submission:** Updated code + README

**Contents:**
- [ ] Complete Phase 3 implementation
- [ ] Updated source code
- [ ] Updated README.txt
- [ ] API documentation
- [ ] Test scripts for file transfer

**Format:** .zip or .tar.gz

---

### Deadline 4: Final Report & Reflection
**Submission:** Report + Personal Reflection

**Performance Report (Max 5 pages):**
- [ ] Executive summary
- [ ] Methodology
- [ ] Experimental results
  - Statistics tables
  - CDF plots
  - Comparison charts
- [ ] Critical evaluation
  - Scalability analysis
  - Bottleneck identification
  - Improvement proposals
- [ ] Conclusion

**Personal Reflection Statement:**
- [ ] Your contribution to the project
- [ ] Other team members' contributions
- [ ] What you learned
- [ ] What you liked/disliked
- [ ] Challenges faced
- [ ] Skills developed

**Format:** PDF

---

## Demonstration Guidelines

### Demo Requirements (15 minutes)
**Timeline:** Week 15

**Checklist:**
- [ ] **Setup (2 min)**
  - Start 10+ nodes
  - Show BS registration
  - Display routing tables

- [ ] **File Display (1 min)**
  - Show files in each node
  - Verify 3-5 files per node

- [ ] **Search Demo (5 min)**
  - Execute queries from `queries.txt`
  - Show full name search
  - Show partial name search
  - Display search results
  - Show hop counts and latency

- [ ] **File Transfer Demo (3 min)**
  - Download a found file
  - Display file size and hash
  - Verify successful transfer

- [ ] **Failure Recovery (3 min)**
  - Remove 2 random nodes
  - Show system still works
  - Execute searches again

- [ ] **Q&A (1 min)**
  - Be ready to explain design decisions

### Viva Questions (5 minutes)

**Potential Topics:**
- Why did you choose your topology?
- How does your search algorithm work?
- How do you handle network partitions?
- What would you do differently?
- How would your system scale to 1000 nodes?
- What are the main bottlenecks?

**Preparation:**
- [ ] All team members understand the codebase
- [ ] All team members can explain design decisions
- [ ] All team members have reviewed the report
- [ ] Practice demo beforehand

---

## Grading Breakdown

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Design** | 25% | - Clear architecture<br>- Protocol compliance<br>- Scalability considerations<br>- Innovation |
| **Implementation & Demo** | 40% | - Code quality<br>- Functionality<br>- Error handling<br>- Demo success |
| **Final Report** | 25% | - Comprehensive analysis<br>- Clear presentation<br>- Critical evaluation<br>- Professional format |
| **Personal Reflection** | 10% | - Honest self-assessment<br>- Team contribution<br>- Learning outcomes |

---

## Resources & References

### Required Files
- [ ] `file_names.txt` - List of 20 files to share
- [ ] `queries.txt` - List of queries for testing
- [ ] Bootstrap Server code (on Moodle)

### Recommended Tools
- **Programming Languages:** Python, Java, Node.js
- **REST Frameworks:** Flask, FastAPI, Express, Spring Boot
- **Testing:** pytest, JUnit, Jest
- **Visualization:** matplotlib, plotly, seaborn
- **Version Control:** Git

### Useful Commands

```bash
# Check UDP port
netstat -an | grep 5001

# Test UDP connection
nc -u <ip> <port>

# Monitor network traffic
tcpdump -i any udp port 5001

# Check process using port
lsof -i :5001

# Kill process on port
kill -9 $(lsof -t -i:5001)
```

### Documentation Links
- UDP Socket Programming: [language-specific documentation]
- REST API Best Practices
- SHA-256 Hashing: [crypto library documentation]
- Matplotlib CDF Plotting

---

## Team Collaboration Tips

### Task Distribution
- **Member 1:** Bootstrap integration, networking
- **Member 2:** Search algorithm, routing
- **Member 3:** File transfer, REST API
- **Member 4:** Statistics, performance analysis
- **Member 5:** Testing, documentation, integration

### Communication
- [ ] Weekly team meetings
- [ ] Use version control (Git)
- [ ] Code reviews before merging
- [ ] Shared documentation (Google Docs)
- [ ] Task tracking (Trello/Jira)

### Version Control Workflow

```bash
# Create feature branch
git checkout -b feature/search-implementation

# Commit changes
git add .
git commit -m "Implement search forwarding logic"

# Push to remote
git push origin feature/search-implementation

# Create pull request for review
```

---

## Success Criteria

### Minimum Requirements
✅ 10+ nodes running simultaneously  
✅ All nodes registered with BS  
✅ Files distributed (3-5 per node)  
✅ Search works for full and partial names  
✅ File download with hash verification  
✅ System survives 2 node failures  
✅ All statistics collected  
✅ Report completed (max 5 pages)  

### Excellence Indicators
🌟 Efficient search algorithm (low hops)  
🌟 Fast query resolution (low latency)  
🌟 Robust error handling  
🌟 Clean, documented code  
🌟 Comprehensive performance analysis  
🌟 Innovative improvements proposed  
🌟 Professional presentation  

---

## Final Checklist

### Before Submission
- [ ] All code compiles/runs without errors
- [ ] README has clear instructions
- [ ] No executables in submission
- [ ] All files compressed (.zip or .tar.gz)
- [ ] Design document ≤ 3 pages
- [ ] Performance report ≤ 5 pages
- [ ] Personal reflection completed
- [ ] All team members reviewed submission
- [ ] Submitted to Moodle before deadline

### Before Demo
- [ ] All nodes tested and working
- [ ] Demo script prepared
- [ ] All team members present
- [ ] Backup plan if something fails
- [ ] Questions anticipated and answers prepared

---

## Good Luck! 🚀

Remember:
- Start early, test often
- Follow the protocol specifications exactly
- Ask instructor for clarification when needed
- Participate in discussions on Yammer
- Help your team members
- Document everything
- Learn and enjoy the process!

---

**Last Updated:** October 16, 2025  
**Project Duration:** ~15 weeks  
**Team Size:** 5 members  
**Contact:** Check Moodle for instructor contact info
