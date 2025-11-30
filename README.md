# Overlay-Based Distributed Content Searching System

A distributed peer-to-peer (P2P) file sharing system implementation for university coursework. Nodes form an unstructured overlay network, search for files using UDP-based flooding, and transfer files reliably using REST API (Flask).

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
   cd C:\your_file_path\overlay_based_distributed_system
   ```
   
   **macOS/Linux:**
   ```bash
   cd /your_file_path/overlay_based_distributed_system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Dependencies include:
   - `flask` - REST API server
   - `requests` - HTTP client for file downloads
   - `pandas`, `matplotlib`, `numpy` - Performance analysis and plotting

## Quick Start

### Option 1: Automated Demo (5 Nodes)

1. **Run demo:**
   
   **Windows:**
   ```cmd
   run_demo.bat
   ```
   
   **macOS/Linux:**
   ```bash
   chmod +x run_demo.sh
   ./run_demo.sh
   ```
   
   This starts:
   - Bootstrap Server on port **5555**
   - 5 auto-registered nodes (ports 5001-5005)
   - Logs written to `logs/` directory

2. **Start your interactive node** (in a new terminal/command prompt):
   
   **Windows:**
   ```cmd
   python src\node.py --port 5006 --username my_node --bs-ip 127.0.0.1 --bs-port 5555
   ```
   
   **macOS/Linux:**
   ```bash
   python3 src/node.py --port 5006 --username my_node --bs-ip 127.0.0.1 --bs-port 5555
   ```

3. **Register and interact:**
   ```
   > register
   > search lord
   > download <ip> <port> <filename>
   > stats
   > leave
   ```

4. **Stop the network:**
   
   **Windows:** Close the individual command prompt windows
   
   **macOS/Linux:** Press `Ctrl+C` in the terminal running `run_demo.sh`

### Option 2: Manual Setup (10+ Nodes for Phase 4)

1. **Start Bootstrap Server:**
   
   **Windows:**
   ```cmd
   python src\bootstrap_server.py 5000
   ```
   
   **macOS/Linux:**
   ```bash
   python3 src/bootstrap_server.py 5000
   ```

2. **Start 10 nodes** (each in separate terminal/command prompt):
   
   **Windows:**
   ```cmd
   REM Node 1
   python src\node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM Node 2
   python src\node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   
   REM ... Repeat for nodes 3-10 (ports 5003-5010)
   ```
   
   **macOS/Linux:**
   ```bash
   # Node 1
   python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000
   
   # Node 2
   python3 src/node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   
   # ... Repeat for nodes 3-10 (ports 5003-5010)
   ```

3. **Register each node:**
   Type `register` in each node's terminal

4. **Run queries from 3 random nodes:**
   ```
   > run-queries
   ```

See `QUICK_START.md` for detailed Phase 4 testing instructions.

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

## Search Algorithm

- **Method**: Unstructured flooding with TTL
- **Transport**: UDP sockets
- **Matching**: Word-boundary matching (case-insensitive)
  - ✅ `"Lord"` matches `"Lord of the rings"`
  - ✅ `"Happy"` matches `"Happy feet"`
  - ❌ `"Lo"` does NOT match `"Lord of the rings"` (incomplete word)

## File Transfer

- **Protocol**: REST API (Flask server per node)
- **Transport**: TCP (HTTP)
- **File Size**: Randomly generated 2-10 MB
- **Integrity**: SHA-256 hash verification
- **Process**:
  1. Search finds node with file
  2. Issue `download` command with peer's IP/port
  3. File content randomly generated
  4. Hash calculated and displayed
  5. Integrity verified on both ends

## Performance Analysis

### Metrics Collected

- **Latency**: Time to resolve each query (milliseconds)
- **Hops**: Number of application-level hops per query
- **Messages per Node**: Total messages sent/received per node
- **Node Degree**: Routing table size (number of neighbors)
- **Query Statistics**: Queries received, forwarded, answered per node
- **Costs**: Per-query cost and per-node cost

### Generate Analysis Plots

```bash
python3 src/plot_stats.py
```

**Output**: CDF (Cumulative Distribution Function) plots
- `cdf_latency.png` - Query latency distribution
- `cdf_hops.png` - Hop count distribution
- `cdf_messages.png` - Messages per node distribution
- `cdf_node_degree.png` - Node degree distribution

### Statistical Analysis

For each metric, the system calculates:
- Minimum
- Maximum
- Average
- Standard Deviation

See `QUICK_START.md` for complete Phase 4 testing checklist.

## Protocol Specification

The system implements a character-based protocol for easy debugging:

### Message Format
```
<length> <COMMAND> <parameters>
```

- **Length**: 4-digit message length (includes the 4 digits)
- **Command**: Uppercase command name
- **Parameters**: Space-separated values

### Supported Messages

| Message | Format | Description |
|---------|--------|-------------|
| `REG` | `length REG IP port username` | Register with Bootstrap Server |
| `REGOK` | `length REGOK no_nodes [IP port]*` | Registration response |
| `UNREG` | `length UNREG IP port username` | Unregister from Bootstrap Server |
| `UNROK` | `length UNROK value` | Unregistration response |
| `JOIN` | `length JOIN IP port` | Join overlay network |
| `JOINOK` | `length JOINOK value` | Join response |
| `LEAVE` | `length LEAVE IP port` | Leave overlay network |
| `LEAVEOK` | `length LEAVEOK value` | Leave response |
| `SER` | `length SER IP port "filename" hops` | Search for file |
| `SEROK` | `length SEROK no_files IP port hops file1 ...` | Search results |
| `ERROR` | `length ERROR` | Generic error message |

**Example:**
```
0036 REG 127.0.0.1 5001 node1
0014 REGOK 0
```

### Testing Protocol with netcat

```bash
# Connect to Bootstrap Server
nc -u 127.0.0.1 5000

# Send commands manually
0036 REG 127.0.0.1 5001 testnode
```

Full protocol specification in `PROJECT_TASK.md` Section 4.

## Project Structure

```
overlay_based_distributed_system/
├── src/
│   ├── node.py                    # Main node implementation (UDP + REST API)
│   ├── bootstrap_server.py        # Bootstrap Server (manages node registry)
│   ├── bootstrap_client.py        # Client for BS communication
│   ├── bootstrap_manager.py       # BS manager helper
│   ├── search_engine.py           # Search/flooding algorithm implementation
│   ├── file_manager.py            # File generation, hashing, storage
│   ├── protocol.py                # Protocol message parsing/formatting
│   ├── routing_table.py           # Neighbor/routing table management
│   ├── statistics.py              # Performance metrics collection
│   ├── plot_stats.py              # Statistical analysis and CDF plotting
│   └── automated_query_runner.py  # Automated query execution
├── tests/
│   └── test_comprehensive.py      # Comprehensive test suite
├── logs/                           # Performance logs (auto-generated)
│   ├── node_*.csv                 # Per-node query logs
│   ├── node_*_summary.csv         # Per-node statistics summary
│   └── *.log                      # Bootstrap and node logs
├── Documents/
│   └── project_guide.txt          # Additional documentation
├── file_names.txt                 # Pool of 20 file names
├── queries.txt                    # Test queries (50 queries)
├── requirements.txt               # Python dependencies
├── run_demo.sh                    # Automated demo script
├── README.md                      # This file
├── QUICK_START.md                 # Phase 4 testing guide
└── PROJECT_TASK.md                # Complete project specification
```

## Testing

### Run Comprehensive Tests

**Windows:**
```cmd
python tests\test_comprehensive.py
```

**macOS/Linux:**
```bash
python3 tests/test_comprehensive.py
```

### Verify Bootstrap Server

**macOS/Linux (using netcat):**
```bash
# Terminal 1
python3 src/bootstrap_server.py 5000

# Terminal 2 - Test with netcat
nc -u 127.0.0.1 5000
0036 REG 127.0.0.1 5001 testnode
```

**Windows:** Use a UDP client tool or test directly with Python scripts

### Phase 4 Testing Checklist
See `QUICK_START.md` for complete testing procedure:
- ✅ 10 nodes running
- ✅ All nodes registered
- ✅ Query testing from 3 random nodes
- ✅ Statistics collection from ALL nodes
- ✅ Graceful node removal (2 nodes)
- ✅ Repeat query testing
- ✅ Generate CDF plots
- ✅ Calculate min/max/avg/stddev

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

## Troubleshooting

### Node Registration Issues

**Error: "9998 - Already registered"**
```bash
# Solution: Unregister first
> leave
> exit
# Restart with different port or username
```

### File Not Found

**Remember word-boundary matching:**
- `"Lord"` ✅ matches `"Lord of the rings"`
- `"Lo"` ❌ does NOT match `"Lord of the rings"`

### No Neighbors Showing

```bash
# Wait 2-3 seconds after registration
> neighbors
```

### Bootstrap Server Connection Failed

**Windows:**
```cmd
REM Check if BS is running
tasklist | findstr python

REM Check port availability
netstat -an | findstr 5000

REM Restart BS if needed
python src\bootstrap_server.py 5000
```

**macOS/Linux:**
```bash
# Check if BS is running
ps aux | grep bootstrap_server.py

# Check port availability
netstat -an | grep 5000

# Restart BS if needed
python3 src/bootstrap_server.py 5000
```

## Project Team

This is a group project for distributed systems coursework (5 students per group).

## Grading Breakdown

- **Design**: 25% - Network topology, protocol design, system architecture
- **Implementation & Demo**: 40% - Working system with 10+ nodes, file search/transfer
- **Performance Analysis**: 25% - Statistical analysis, CDF plots, critical evaluation
- **Personal Reflection**: 10% - Individual contributions and learnings

## Documentation

- **`PROJECT_TASK.md`** - Complete project specification and requirements
- **`QUICK_START.md`** - Detailed Phase 4 testing instructions with checklist
- **`project_description.txt`** - Original project brief
- **`Documents/project_guide.txt`** - Implementation guidance

## Credits

This project is derived from:
- **Dr. Dilum Bandara** - Original project design
- **Dr. Anura P. Jayasumana** - ECE 658 Internet Engineering, Colorado State University, 2012
- **Vidarshana Bandara** - Further enhancements

## License

Academic project for educational purposes only.

---

**For complete testing procedure, see `QUICK_START.md`**  
**For project requirements, see `PROJECT_TASK.md`**
