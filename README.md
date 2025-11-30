# Overlay-Based Distributed Content Searching System

A distributed peer-to-peer (P2P) file sharing system implementation for university coursework. Nodes form an unstructured overlay network, search for files using UDP-based flooding, and transfer files reliably using REST API (Flask).

## Table of Contents

1. [Overview](#overview)
2. [Project Phases](#project-phases)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Quick Start](#quick-start)
   - [Quick Testing (3-5 Nodes)](#quick-testing-3-5-nodes)
   - [Phase 4 Testing (10+ Nodes)](#phase-4-testing-10-nodes)
6. [Available Commands](#available-commands)
7. [System Architecture](#system-architecture)
8. [Performance Analysis](#performance-analysis)
9. [Protocol Specification](#protocol-specification)
10. [Project Structure](#project-structure)
11. [Testing](#testing)
12. [Expected Performance](#expected-performance)
13. [Search Algorithm Details](#search-algorithm-details)
14. [File Transfer Details](#file-transfer-details)
15. [Troubleshooting](#troubleshooting)
16. [Project Team](#project-team)
17. [Grading Breakdown](#grading-breakdown)
18. [Documentation](#documentation)
19. [Credits](#credits)
20. [License](#license)

## Overview

This project implements a distributed content searching system where:
- **10+ nodes** share **20 files** (3-5 files per node)
- Nodes connect to the network via a **Bootstrap Server**
- File search uses **UDP flooding** with word-boundary matching
- File transfer uses **TCP-based REST API** with SHA-256 integrity verification
- System handles **graceful node departures** and continues operating
- Comprehensive **performance metrics** collection and analysis

## Project Phases

1. **Phase 1**: Network topology formation and node content initialization
2. **Phase 2**: UDP-based socket communication for file search (flooding algorithm)
3. **Phase 3**: REST API implementation for reliable file transfer with integrity verification
4. **Phase 4**: Performance analysis with statistical metrics and CDF plots

See `PROJECT_TASK.md` for complete project requirements.

## Prerequisites

- **Python 3.8+**
- **pip** package manager
- **Windows, macOS, or Linux**

## Installation

1. **Navigate to project directory:**
   
   **Windows:**
   ```cmd
   cd C:\path\to\overlay_based_distributed_system
   ```
   
   **macOS/Linux:**
   ```bash
   cd /path/to/overlay_based_distributed_system
   ```
   
   Replace `path/to` with your actual project location.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Dependencies include:
   - `flask` - REST API server
   - `requests` - HTTP client for file downloads
   - `pandas`, `matplotlib`, `numpy` - Performance analysis and plotting

## Quick Start

> **Note for macOS users:** Port 5000 is often used by AirPlay Receiver. If you get "Address already in use" error, use port 5555 instead:
> ```bash
> python3 src/bootstrap_server.py 5555
> # Then use --bs-port 5555 when starting nodes
> ```

### Quick Testing (3-5 Nodes)

1. **Start Bootstrap Server** (Terminal 1):
   
   **Windows:**
   ```cmd
   python src\bootstrap_server.py 5000
   ```
   
   **macOS/Linux:**
   ```bash
   python3 src/bootstrap_server.py 5000
   ```
   
   **If port 5000 is in use (macOS):**
   ```bash
   python3 src/bootstrap_server.py 5555
   ```

2. **Start 3-5 nodes** (each in separate terminal/command prompt):
   
   **Terminal 2 - Node 1:**
   ```cmd
   REM Windows
   python src\node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   ```
   ```bash
   # macOS/Linux
   python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   ```
   
   **Terminal 3 - Node 2:**
   ```cmd
   REM Windows
   python src\node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   ```
   ```bash
   # macOS/Linux
   python3 src/node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   ```
   
   **Terminal 4 - Node 3:**
   ```cmd
   REM Windows
   python src\node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5000
   ```
   ```bash
   # macOS/Linux
   python3 src/node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5000
   ```

3. **Register each node:**
   In each node's terminal window, type:
   ```
   > register
   ```
   Wait 2-3 seconds for network stabilization.

4. **Test search functionality:**
   In any node's terminal:
   ```
   > search lord
   > search twilight
   > search american
   ```

5. **View node information:**
   ```
   > files       # Show files hosted by this node
   > neighbors   # Show connected peers
   > stats       # Show performance metrics
   ```

6. **Download a file:**
   ```
   > download 127.0.0.1 5002 "Twilight.mp3"
   ```
   Replace IP, port, and filename with actual values from search results.

7. **Gracefully exit:**
   ```
   > leave
   ```

### Phase 4 Testing (10+ Nodes)

For comprehensive performance analysis, you need to run the full Phase 4 testing procedure with 10+ nodes. This requires **11 terminal windows** (1 Bootstrap Server + 10 Nodes).

1. **Start Bootstrap Server** (Terminal 1):
   
   **Windows:**
   ```cmd
   python src\bootstrap_server.py 5000
   ```
   
   **macOS/Linux:**
   ```bash
   python3 src/bootstrap_server.py 5000
   ```

2. **Start 10 nodes** (Terminals 2-11, one node per terminal):
   
   Use the following commands, opening each in a **separate** terminal/command prompt:
   
   **Windows:**
   ```cmd
   REM Terminal 2 - Node 1
   python src\node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 3 - Node 2
   python src\node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 4 - Node 3
   python src\node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 5 - Node 4
   python src\node.py --port 5004 --username node4 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 6 - Node 5
   python src\node.py --port 5005 --username node5 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 7 - Node 6
   python src\node.py --port 5006 --username node6 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 8 - Node 7
   python src\node.py --port 5007 --username node7 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 9 - Node 8
   python src\node.py --port 5008 --username node8 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 10 - Node 9
   python src\node.py --port 5009 --username node9 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Terminal 11 - Node 10
   python src\node.py --port 5010 --username node10 --bs-ip 127.0.0.1 --bs-port 5000
   ```
   
   **macOS/Linux:**
   ```bash
   # Terminal 2 - Node 1
   python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 3 - Node 2
   python3 src/node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 4 - Node 3
   python3 src/node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 5 - Node 4
   python3 src/node.py --port 5004 --username node4 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 6 - Node 5
   python3 src/node.py --port 5005 --username node5 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 7 - Node 6
   python3 src/node.py --port 5006 --username node6 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 8 - Node 7
   python3 src/node.py --port 5007 --username node7 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 9 - Node 8
   python3 src/node.py --port 5008 --username node8 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 10 - Node 9
   python3 src/node.py --port 5009 --username node9 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 11 - Node 10
   python3 src/node.py --port 5010 --username node10 --bs-ip 127.0.0.1 --bs-port 5000
   ```

3. **Register all nodes:**
   In each of the 10 node terminals, type:
   ```
   > register
   ```
   Wait 3-5 seconds for network stabilization.

4. **Run automated queries from 3 random nodes:**
   
   Choose any 3 nodes (e.g., node3, node5, node8) and run:
   ```
   > run-queries
   ```
   
   This executes all queries from `queries.txt` and logs results to `logs/` directory.

5. **Collect statistics from ALL 10 nodes:**
   
   In each node's terminal, type:
   ```
   > stats
   ```
   
   Statistics are automatically saved to:
   - `logs/node_127.0.0.1_<port>.csv` - Per-query details
   - `logs/node_127.0.0.1_<port>_summary.csv` - Aggregate statistics

6. **Test graceful node removal:**
   
   Choose any 2 nodes (e.g., node9 and node10) and gracefully remove them:
   ```
   > leave
   ```
   
   Wait 2-3 seconds for network stabilization.

7. **Repeat query testing** (with 8 remaining nodes):
   
   Choose 3 different nodes and run:
   ```
   > run-queries
   ```

8. **Collect final statistics** from remaining nodes:
   ```
   > stats
   ```

9. **Generate performance analysis plots:**
   
   In a new terminal, run:
   ```bash
   python3 src/plot_stats.py
   ```
   
   This generates CDF plots:
   - `cdf_latency.png` - Query latency distribution
   - `cdf_hops.png` - Hop count distribution
   - `cdf_messages.png` - Messages per node
   - `cdf_node_degree.png` - Node degree distribution

10. **Analyze results:**
    
    Review the generated statistics and plots:
    - Minimum, Maximum, Average, Standard Deviation for each metric
    - Compare performance before and after node removal
    - Evaluate network resilience and efficiency

For a detailed step-by-step checklist, see `QUICK_START.md`.

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `register` | Register with Bootstrap Server and join network | `register` |
| `search <query>` | Search for files (supports partial matching) | `search twilight` |
| `download <ip> <port> <file>` | Download file from peer with integrity check | `download 127.0.0.1 5002 "Twilight.mp3"` |
| `run-queries` | Run all queries from queries.txt automatically | `run-queries` |
| `files` | Display files hosted by this node | `files` |
| `neighbors` | Show routing table (connected peers) | `neighbors` |
| `stats` | Display performance statistics | `stats` |
| `leave` | Gracefully leave network (notifies all neighbors) | `leave` |
| `exit` | Force quit without cleanup | `exit` |

## System Architecture

### Components

1. **Bootstrap Server** (`bootstrap_server.py`)
   - Central registry for active nodes
   - Provides up to 2 random peers to new nodes
   - Handles registration and unregistration
   - **Port**: Configurable (default 5000)

2. **Node** (`node.py`)
   - **UDP Listener**: Receives search queries (flooding)
   - **REST API Server**: Flask server for file downloads (TCP)
   - **Bootstrap Client**: Registers with Bootstrap Server
   - **Search Engine**: Implements flooding algorithm with TTL
   - **File Manager**: Generates files (2-10 MB), computes SHA-256 hashes
   - **Routing Table**: Maintains neighbor list (2-4 neighbors per node)
   - **Statistics Collector**: Logs latency, hops, messages, queries

3. **Supporting Modules**
   - `search_engine.py` - Flooding algorithm implementation
   - `file_manager.py` - File generation, storage, hashing
   - `protocol.py` - Message parsing and formatting
   - `routing_table.py` - Neighbor management
   - `statistics.py` - Performance metrics collection
   - `plot_stats.py` - Statistical analysis and CDF plotting
   - `automated_query_runner.py` - Automated query execution

### Network Topology

- **Type**: Unstructured overlay network
- **Initial connections**: 2 neighbors per node (from Bootstrap Server)
- **Stabilized connections**: 2-4 neighbors per node
- **Diameter**: 3-5 hops (10-node network)
- **Join process**:
  1. Node contacts Bootstrap Server
  2. Bootstrap Server returns 2 random active peers
  3. Node sends JOIN messages to peers
  4. Peers add node to routing tables
  5. Network stabilizes over time

### File Search Process

1. Node issues search query (e.g., `search lord`)
2. Query floods through network (UDP messages)
3. TTL decrements at each hop (prevents infinite loops)
4. Nodes with matching files respond with SEROK
5. Search results displayed at originating node
6. User can download files using REST API

### File Transfer Process

1. User issues download command: `download <ip> <port> <filename>`
2. Node sends HTTP GET request to peer's REST API
3. Peer generates file content (random 2-10 MB)
4. Peer computes SHA-256 hash
5. Peer sends file + hash in HTTP response header
6. Downloading node verifies integrity
7. File saved to local storage

### Statistics Collection

**Real-time tracking** (`statistics.py`):
- Queries received, forwarded, answered
- Per-query latency (milliseconds)
- Per-query hops
- Messages sent/received per node
- Node degree (neighbor count)

**Logging**:
- `logs/node_<ip>_<port>.csv` - Per-query details
- `logs/node_<ip>_<port>_summary.csv` - Aggregate statistics

**Analysis** (`plot_stats.py`):
- Reads CSV logs from all nodes
- Calculates min, max, avg, stddev
- Generates CDF plots (PNG files)

## Performance Analysis

### Metrics Collected

- **Latency**: Time to resolve each query (milliseconds)
- **Hops**: Number of application-level hops per query
- **Messages per Node**: Total messages sent/received per node
- **Node Degree**: Routing table size (number of neighbors)
- **Query Statistics**: Queries received, forwarded, answered per node
- **Per-Query Cost**: Messages required to resolve a single query
- **Per-Node Cost**: Total messages processed by each node

### Implementation Details

**Statistics Tracking** (`src/statistics.py`):
- Real-time counters for all metrics
- Automatic CSV logging to `logs/` directory
- Methods:
  - `record_query_received()` - Increment received counter
  - `record_query_forwarded()` - Increment forwarded counter
  - `record_query_answered()` - Increment answered counter
  - `print_stats()` - Display current metrics
  - `save_summary()` - Write aggregate stats to CSV

**Data Collection Process:**
1. Each node tracks performance in real-time
2. Use `stats` command to display and save metrics
3. CSV files generated in `logs/` directory
4. Statistics persist across testing phases

### Generate Analysis Plots

After collecting statistics from all nodes, generate CDF plots:

**Windows:**
```cmd
python src\plot_stats.py
```

**macOS/Linux:**
```bash
python3 src/plot_stats.py
```

**Output Files:**
- `cdf_latency.png` - Query latency distribution
- `cdf_hops.png` - Hop count distribution
- `cdf_messages.png` - Messages per node distribution
- `cdf_node_degree.png` - Node degree distribution

**Statistical Calculations:**
For each metric, the system calculates:
- **Minimum** - Lowest observed value
- **Maximum** - Highest observed value
- **Average** - Mean across all observations
- **Standard Deviation** - Measure of variability

### Expected Performance

**Network with 10 nodes:**
- **Neighbors per node**: 2 (initial) → 2-4 (after stabilization)
- **Network diameter**: 3-5 hops
- **Query success rate**: 85-95%
- **Average latency**: 20-80 ms
- **Average hops**: 2-3
- **Messages per query**: 8-15 (flooding overhead)

**After removing 2 nodes (8 nodes):**
- **Success rate**: 75-90% (slight degradation)
- **Average hops**: 2-4 (may increase)
- **Network**: Remains functional and self-healing

### Analysis Guidelines

Compare metrics before and after node removal to evaluate:
1. **Network resilience** - Does the network continue functioning?
2. **Performance degradation** - How much do metrics worsen?
3. **Scalability** - Is flooding efficient for this topology?
4. **Reliability** - What percentage of queries succeed?

See `QUICK_START.md` for complete Phase 4 testing checklist.

## Protocol Specification

The system implements a character-based protocol for easy debugging:

### Message Format
```
<length> <COMMAND> <parameters>
```

- **Length**: 4-digit message length (includes the 4 length digits)
- **Command**: Uppercase command name
- **Parameters**: Space-separated values

### Supported Messages

| Message | Format | Description |
|---------|--------|-------------|
| `REG` | `length REG IP port username` | Register with Bootstrap Server |
| `REGOK` | `length REGOK no_nodes [IP port]*` | Registration response (0-2 peers) |
| `UNREG` | `length UNREG IP port username` | Unregister from Bootstrap Server |
| `UNROK` | `length UNROK value` | Unregistration response (0=success) |
| `JOIN` | `length JOIN IP port` | Join overlay network (sent to peers) |
| `JOINOK` | `length JOINOK value` | Join response (0=success) |
| `LEAVE` | `length LEAVE IP port` | Leave overlay network |
| `LEAVEOK` | `length LEAVEOK value` | Leave response (0=success) |
| `SER` | `length SER IP port "filename" hops` | Search for file |
| `SEROK` | `length SEROK no_files IP port hops file1 file2 ...` | Search results |
| `ERROR` | `length ERROR` | Generic error message |

### Message Examples

**Registration:**
```
Request:  0036 REG 127.0.0.1 5001 node1
Response: 0051 REGOK 2 127.0.0.1 5002 127.0.0.1 5003
```

**Search Query:**
```
Request:  0042 SER 127.0.0.1 5001 "Lord of the rings" 5
Response: 0068 SEROK 2 127.0.0.1 5003 4 "Lord of the rings.txt" "Lord.mp3"
```

**Join Network:**
```
Request:  0028 JOIN 127.0.0.1 5005
Response: 0016 JOINOK 0
```

**Leave Network:**
```
Request:  0029 LEAVE 127.0.0.1 5005
Response: 0017 LEAVEOK 0
```

### Testing Protocol with netcat

You can test the protocol manually using netcat:

**macOS/Linux:**
```bash
# Terminal 1 - Start Bootstrap Server
python3 src/bootstrap_server.py 5000

# Terminal 2 - Test with netcat
nc -u 127.0.0.1 5000
0036 REG 127.0.0.1 5001 testnode
# Expected response: 0014 REGOK 0 (no other nodes yet)
```

**Windows:**
Use a UDP client tool or test directly with Python scripts.

Full protocol specification in `PROJECT_TASK.md` Section 4.

## Project Structure

```
overlay_based_distributed_system/
├── src/                            # Source code
│   ├── node.py                     # Main node (UDP listener + REST API)
│   ├── bootstrap_server.py         # Bootstrap Server (node registry)
│   ├── bootstrap_client.py         # Bootstrap communication client
│   ├── bootstrap_manager.py        # Bootstrap manager helper
│   ├── search_engine.py            # Flooding search algorithm
│   ├── file_manager.py             # File generation and hashing
│   ├── protocol.py                 # Protocol message parsing
│   ├── routing_table.py            # Neighbor/routing management
│   ├── statistics.py               # Performance metrics collection
│   ├── plot_stats.py               # Statistical analysis and CDF plots
│   └── automated_query_runner.py   # Automated query execution
├── tests/                          # Test suite
│   └── test_comprehensive.py       # Comprehensive system tests
├── logs/                           # Performance logs (auto-generated)
│   ├── node_*.csv                  # Per-node query logs
│   ├── node_*_summary.csv          # Per-node statistics
│   └── *.log                       # Bootstrap and node logs
├── Documents/                      # Additional documentation
│   └── project_guide.txt           # Implementation guidance
├── file_names.txt                  # Pool of 20 file names
├── queries.txt                     # Test queries (50 queries)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── QUICK_START.md                  # Phase 4 testing guide
└── PROJECT_TASK.md                 # Complete project specification
```

### Key Files

- **`src/node.py`**: Main node implementation
  - UDP listener for search queries (lines 144-185)
  - REST API server for file downloads (lines 113-142)
  - Download client with integrity verification (lines 297-331)
  - Command-line interface for user interaction

- **`src/statistics.py`**: Performance tracking
  - Real-time counters for queries, messages, latency
  - CSV logging functionality
  - Summary statistics generation

- **`src/search_engine.py`**: Search implementation
  - Flooding algorithm with TTL
  - Word-boundary matching
  - Query deduplication

- **`src/file_manager.py`**: File operations
  - Random file generation (2-10 MB)
  - SHA-256 hash computation
  - File storage and retrieval

- **`file_names.txt`**: 20 movie/music titles for file names
- **`queries.txt`**: 50 test queries for automated testing

## Testing

### Quick Functionality Test

Test basic functionality with 3 nodes:

1. **Start Bootstrap Server** (Terminal 1):
   ```bash
   python3 src/bootstrap_server.py 5000
   ```

2. **Start 3 nodes** (Terminals 2-4):
   ```bash
   # Terminal 2
   python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 3
   python3 src/node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Terminal 4
   python3 src/node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5000
   ```

3. **Register all nodes:**
   ```
   > register
   ```

4. **Test search:**
   ```
   > search lord
   > files
   > neighbors
   ```

### Comprehensive Test Suite

Run automated tests:

**Windows:**
```cmd
python tests\test_comprehensive.py
```

**macOS/Linux:**
```bash
python3 tests/test_comprehensive.py
```

### Bootstrap Server Verification

Test Bootstrap Server protocol manually:

**macOS/Linux:**
```bash
# Terminal 1 - Start Bootstrap Server
python3 src/bootstrap_server.py 5000

# Terminal 2 - Test with netcat
nc -u 127.0.0.1 5000
0036 REG 127.0.0.1 5001 testnode
# Expected: 0014 REGOK 0
```

**Windows:**
Use Python scripts or a UDP client tool to send test messages.

### Phase 4 Full Testing

For complete Phase 4 performance evaluation:

1. **Setup**: 10 nodes + Bootstrap Server (11 terminals)
2. **Initial Testing**: Run queries from 3 random nodes
3. **Collect Statistics**: From all 10 nodes
4. **Node Removal**: Gracefully remove 2 nodes
5. **Repeat Testing**: Run queries with remaining 8 nodes
6. **Final Statistics**: Collect from remaining nodes
7. **Generate Plots**: Create CDF visualizations
8. **Analysis**: Compare before/after metrics

See `QUICK_START.md` for detailed step-by-step checklist.

## Expected Performance

**Network with 10 nodes:**
- **Neighbors per node**: 2 (initial) → 2-4 (after stabilization)
- **Network diameter**: 3-5 hops
- **Query success rate**: 85-95%
- **Average latency**: 20-80 ms
- **Average hops**: 2-3
- **Messages per query**: 8-15 (flooding overhead)

**After removing 2 nodes (8 nodes):**
- **Success rate**: 75-90% (slight degradation)
- **Average hops**: 2-4 (may increase)
- **Network**: Remains functional

## Search Algorithm Details

The system uses **unstructured flooding** with TTL for file discovery:

**Algorithm:**
- **Method**: Unstructured flooding with Time-To-Live (TTL)
- **Transport**: UDP sockets for fast, lightweight message passing
- **TTL**: Decrements at each hop (default: 5 hops max)
- **Query Deduplication**: Prevents reprocessing same query

**Matching Rules:**
- **Case-insensitive** word-boundary matching
- ✅ `"Lord"` matches `"Lord of the rings.txt"`
- ✅ `"Happy"` matches `"Happy feet.mp3"`
- ✅ `"american"` matches `"American Beauty.mp3"`
- ❌ `"Lo"` does NOT match `"Lord of the rings"` (incomplete word)
- ❌ `"beau"` does NOT match `"American Beauty"` (partial word)

**Process:**
1. User issues search: `search lord`
2. Node creates SER message with TTL=5
3. Query floods to all neighbors via UDP
4. Each receiving node:
   - Checks for duplicate (skip if seen before)
   - Searches local files for word-boundary matches
   - Sends SEROK if files found
   - Decrements TTL and forwards to neighbors (if TTL > 0)
5. Originating node collects all SEROK responses
6. Results displayed to user with IP, port, filename, hops

**Implementation:** See `src/search_engine.py`

## File Transfer Details

Files are transferred using a **REST API** with SHA-256 integrity verification:

**Protocol:**
- **Method**: HTTP GET request
- **Transport**: TCP (reliable delivery)
- **Server**: Flask (per-node REST API)
- **Endpoint**: `GET /download/<filename>`
- **File Size**: Randomly generated 2-10 MB per file
- **Integrity**: SHA-256 hash in response header

**Process:**
1. User finds file via search: `search twilight`
2. Search returns: `127.0.0.1 5003 "Twilight.mp3" (2 hops)`
3. User issues download: `download 127.0.0.1 5003 "Twilight.mp3"`
4. Downloading node sends HTTP GET to `http://127.0.0.1:<rest_port>/download/Twilight.mp3`
5. Serving node:
   - Generates file content (random bytes, 2-10 MB)
   - Computes SHA-256 hash
   - Sends file with hash in `X-File-Hash` header
6. Downloading node:
   - Receives file content
   - Computes SHA-256 hash locally
   - Verifies hash matches header
   - Saves file to local storage
7. Success message displayed with file size and hash

**Implementation:**
- REST API Server: `src/node.py` lines 113-142
- Download Client: `src/node.py` lines 297-331
- File Generation: `src/file_manager.py`

**Security:** SHA-256 ensures file integrity and detects corruption/tampering.

## Troubleshooting

### Node Registration Issues

**Problem: "9998 - Already registered"**

**Solution:**
```bash
# In the node terminal
> leave
> exit

# Restart node with different port or username
python3 src/node.py --port 5011 --username new_node --bs-ip 127.0.0.1 --bs-port 5000
```

**Problem: "Registration failed"**

**Causes:**
- Bootstrap Server not running
- Wrong Bootstrap Server IP/port
- Network connectivity issues
- Port 5000 already in use (common on macOS - AirPlay uses this port)

**Solution:**
```bash
# Verify Bootstrap Server is running
ps aux | grep bootstrap_server.py  # macOS/Linux
tasklist | findstr python          # Windows

# Check port availability
netstat -an | grep 5000            # macOS/Linux
netstat -an | findstr 5000         # Windows

# If port 5000 is occupied (common on macOS), use a different port
python3 src/bootstrap_server.py 5555

# Then update nodes to use the new port
python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5555

# Restart Bootstrap Server
python3 src/bootstrap_server.py 5000
```

### File Search Issues

**Problem: "File not found" when it should exist**

**Remember:** Word-boundary matching required
- ✅ `search lord` matches `"Lord of the rings"`
- ❌ `search lo` does NOT match `"Lord of the rings"`

**Solution:**
Use complete words in search queries:
```
> search lord        # Good
> search twilight    # Good
> search lo          # Bad - incomplete word
```

**Problem: No search results from any node**

**Causes:**
- Nodes not connected (no neighbors)
- Network not stabilized yet

**Solution:**
```bash
# Check neighbors
> neighbors

# If empty, wait 3-5 seconds after registration
# Then try search again
> search american
```

### No Neighbors After Registration

**Problem:** `neighbors` command shows empty routing table

**Solution:**
```bash
# Wait 2-3 seconds for network stabilization
# The join process takes time

# Check again
> neighbors

# If still empty, check Bootstrap Server gave peers
# You should see "REGOK" message with peer info when registering
```

### Bootstrap Server Connection Failed

**Problem:** Cannot connect to Bootstrap Server

**Windows Solution:**
```cmd
REM Check if Bootstrap Server is running
tasklist | findstr python

REM Check port availability
netstat -an | findstr 5000

REM Restart Bootstrap Server
python src\bootstrap_server.py 5000
```

**macOS/Linux Solution:**
```bash
# Check if Bootstrap Server is running
ps aux | grep bootstrap_server.py

# Check port availability
netstat -an | grep 5000
lsof -i :5000  # Alternative

# Kill existing process if needed
pkill -f bootstrap_server.py

# Restart Bootstrap Server
python3 src/bootstrap_server.py 5000
```

### File Download Issues

**Problem:** "Download failed" or integrity check failure

**Causes:**
- Target node crashed or left network
- Network connectivity issues
- Port conflicts

**Solution:**
```bash
# 1. Verify target node is still running
# Check in the target node's terminal

# 2. Try downloading from a different node
> search <query>
# Pick a different result

# 3. Check if REST API port is available
> neighbors  # Verify node is still in routing table
```

### Port Already in Use

**Problem:** "Address already in use" error when starting node

**Windows Solution:**
```cmd
REM Find process using the port
netstat -ano | findstr :5001

REM Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

REM Or use a different port
python src\node.py --port 5011 --username node11 --bs-ip 127.0.0.1 --bs-port 5000
```

**macOS/Linux Solution:**
```bash
# Find process using the port
lsof -i :5001

# Kill the process
kill -9 <PID>

# Or use a different port
python3 src/node.py --port 5011 --username node11 --bs-ip 127.0.0.1 --bs-port 5000
```

### Statistics Not Saving

**Problem:** CSV files not created in `logs/` directory

**Causes:**
- `logs/` directory doesn't exist
- Permission issues

**Solution:**
```bash
# Create logs directory manually
mkdir logs          # macOS/Linux
mkdir logs          # Windows (same command)

# Check permissions
ls -la logs/        # macOS/Linux
dir logs\           # Windows

# Run stats command again
> stats
```

### Performance Issues

**Problem:** High latency or query timeouts

**Causes:**
- Network congestion
- Too many nodes on same machine
- Insufficient system resources

**Solution:**
```bash
# 1. Reduce number of nodes
# Use 5-8 nodes instead of 10+

# 2. Increase query timeout
# Edit src/search_engine.py if needed

# 3. Monitor system resources
top          # macOS/Linux
taskmgr      # Windows (Task Manager)
```

### Plot Generation Issues

**Problem:** `plot_stats.py` fails or produces empty plots

**Causes:**
- No CSV files in `logs/` directory
- Missing dependencies (matplotlib, pandas, numpy)
- Insufficient data

**Solution:**
```bash
# 1. Verify CSV files exist
ls logs/node_*.csv                    # macOS/Linux
dir logs\node_*.csv                   # Windows

# 2. Reinstall dependencies
pip install matplotlib pandas numpy

# 3. Ensure you ran queries and collected stats first
# In node terminals:
> run-queries
> stats

# 4. Then generate plots
python3 src/plot_stats.py
```

### Common Errors and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `9998 - Already registered` | Node already in Bootstrap Server | `leave` then restart |
| `9999 - Request failed` | Bootstrap Server unreachable | Check BS is running |
| `Connection refused` | Wrong port or IP | Verify connection parameters |
| `Permission denied` | Port requires admin rights | Use port > 1024 |
| `Address already in use` | Port occupied | Kill process or use different port |
| `Module not found` | Missing dependencies | `pip install -r requirements.txt` |
| `File not found` | Search query too short | Use complete words |

### Getting Help

1. **Check documentation:**
   - `README.md` - This file
   - `QUICK_START.md` - Phase 4 testing guide
   - `PROJECT_TASK.md` - Complete specification

2. **Review logs:**
   - `logs/*.log` - Bootstrap and node logs
   - `logs/node_*.csv` - Query logs

3. **Test incrementally:**
   - Start with Bootstrap Server only
   - Add one node at a time
   - Test each component before proceeding

4. **Clean restart:**
   ```bash
   # Kill all Python processes
   pkill -f python                # macOS/Linux
   taskkill /F /IM python.exe     # Windows
   
   # Clear old logs
   rm -rf logs/*                  # macOS/Linux
   del /Q logs\*                  # Windows
   
   # Start fresh
   ```

## Project Team

This is a group project for distributed systems coursework (5 students per group).

## Grading Breakdown

- **Design**: 25% - Network topology, protocol design, system architecture
- **Implementation & Demo**: 40% - Working system with 10+ nodes, file search/transfer
- **Performance Analysis**: 25% - Statistical analysis, CDF plots, critical evaluation
- **Personal Reflection**: 10% - Individual contributions and learnings

## Documentation

- **`README.md`** - This file (comprehensive project guide)
- **`QUICK_START.md`** - Detailed Phase 4 testing instructions with step-by-step checklist
- **`PROJECT_TASK.md`** - Complete project specification and requirements
- **`Documents/project_guide.txt`** - Implementation guidance and tips

## Credits

This project is derived from:
- **Dr. Dilum Bandara** - Original project design
- **Dr. Anura P. Jayasumana** - ECE 658 Internet Engineering, Colorado State University, 2012
- **Vidarshana Bandara** - Further enhancements

## License

Academic project for educational purposes only.

---

**Need Help?**
- For quick start: See [Quick Start](#quick-start) section above
- For Phase 4 testing: See `QUICK_START.md`
- For troubleshooting: See [Troubleshooting](#troubleshooting) section above
- For project requirements: See `PROJECT_TASK.md`

**Ready to begin?** Start with the [Installation](#installation) section!
