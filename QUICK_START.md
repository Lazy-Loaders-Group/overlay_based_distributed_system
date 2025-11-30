# Quick Start Guide - Phase 4 Testing

## Ready in 5 Minutes!

> **Important for macOS users:** Port 5000 is often used by AirPlay Receiver. If you get "Address already in use" error, use port 5555 instead and update all `--bs-port` values accordingly.

---

## Prerequisites

**Before starting, navigate to the project directory:**

**Windows:**
```cmd
cd C:\path\to\overlay_based_distributed_system
```

**macOS/Linux:**
```bash
cd /path/to/overlay_based_distributed_system
```

Replace `path/to` with your actual project location (e.g., `C:\Users\YourName\Documents\` or `/home/username/projects/`).

**All commands below assume you are already in the project root directory.**

---

## Step 1: Start Bootstrap Server (Terminal 1)

**Windows:**
```cmd
python src\bootstrap_server.py 5000
```

**macOS/Linux:**
```bash
python3 src/bootstrap_server.py 5000
```

**If port 5000 is in use (common on macOS):**
```bash
python3 src/bootstrap_server.py 5555
```
*Remember to use `--bs-port 5555` in all node commands if using this port.*

**Expected:** Server listening on the specified port

---

## Step 2: Start 10 Nodes (Terminals 2-11)

Copy-paste these commands into 10 separate terminals/command prompts:

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

---

## Step 3: Register All Nodes

In **each node terminal**, type:
```
> register
```

**Expected:** "Registered successfully" message

---

## Step 4: Verify Setup

Pick any node and check:
```
> files
> neighbors  
```

**Expected:** 
- 3-5 files listed
- 2 neighbors listed

---

## Step 5: Run Queries (Experiment 1)

**Select 3 random nodes** (example: nodes on ports 5002, 5005, 5008)

In each selected node terminal:
```
> run-queries
Enter query file path (default: queries.txt): [Press Enter]
Delay between queries in seconds (default: 2): [Press Enter]
```

**Wait:** ~2 minutes per node (50 queries × 2 seconds)

---

## Step 6: Collect Statistics from ALL Nodes

**IMPORTANT:** Collect stats from **ALL 10 nodes**, not just the 3 query nodes!

On **EACH of the 10 nodes**:
```
> stats
```

**Record for each node:**
- Queries received
- Queries forwarded
- Queries answered
- Messages sent
- Messages received
- Routing table size (neighbor count)

**Calculate totals across all nodes:**
- Total queries received (sum from all nodes)
- Total queries forwarded (sum from all nodes)
- Total queries answered (sum from all nodes)

---

## Step 7: Remove Nodes ONE AT A TIME (Experiment 2)

**Select 2 random nodes to remove** (example: 5003, 5007)

### Remove First Node:
In terminal for node 5003:
```
> leave
```

**Wait:** 5 seconds for network stabilization

**Check routing tables** on remaining nodes:
```
> neighbors
```
(Node 5003 should be gone from all routing tables)

### Remove Second Node:
In terminal for node 5007:
```
> leave
```

**Wait:** 5 seconds for network stabilization

---

## Step 8: Repeat Queries

On the **same 3 query nodes from Step 5** (if they're still running):
```
> run-queries
[Press Enter twice]
```

Check stats again:
```
> stats
```

---

## Step 9: Collect Statistics AGAIN from ALL Nodes

On **EACH of the remaining 8 nodes**:
```
> stats
```

**Record the same metrics as Step 6** and compare!

---

## Step 10: Generate Analysis Plots

In a new terminal/command prompt (navigate to project directory first):

**Windows:**
```cmd
python src\plot_stats.py
```

**macOS/Linux:**
```bash
python3 src/plot_stats.py
```

**Expected:** 4 CDF plot PNG files:
- `cdf_latency.png` - CDF of query latencies
- `cdf_hops.png` - CDF of hop counts
- `cdf_messages.png` - CDF of messages per node
- `cdf_node_degree.png` - CDF of routing table sizes (neighbors per node)

**Note:** If `cdf_node_degree.png` is missing, you need to manually calculate node degree distribution from routing table sizes collected in Steps 6 and 9.

---

## Step 11: Calculate Required Metrics

### For Both Experiments (Before & After Removal):

**Hops:**
- Min, Max, Average, Standard Deviation

**Latency (ms):**
- Min, Max, Average, Standard Deviation  

**Messages Per Node:**
- Min, Max, Average, Standard Deviation
- Total messages across all nodes

**Node Degree (Routing Table Size):**
- Min, Max, Average, Standard Deviation

**Per Query Cost:**
- Average messages needed to resolve one query
- Formula: `Total Messages / Total Queries`

**Per Node Cost:**
- Average messages handled per node
- Formula: `Total Messages / Number of Nodes`

---

## Step 12: Collect Results

Copy all log files:

**Windows:**
```cmd
xcopy logs logs_experiment_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2% /E /I
```

**macOS/Linux:**
```bash
cp -r logs logs_experiment_$(date +%Y%m%d_%H%M%S)
```

**Create a summary spreadsheet with:**

| Metric | Experiment 1 (10 nodes) | Experiment 2 (8 nodes) |
|--------|------------------------|------------------------|
| Min Hops | | |
| Max Hops | | |
| Avg Hops | | |
| StdDev Hops | | |
| Min Latency (ms) | | |
| Max Latency (ms) | | |
| Avg Latency (ms) | | |
| StdDev Latency (ms) | | |
| Min Messages/Node | | |
| Max Messages/Node | | |
| Avg Messages/Node | | |
| StdDev Messages/Node | | |
| Min Node Degree | | |
| Max Node Degree | | |
| Avg Node Degree | | |
| StdDev Node Degree | | |
| Total Queries Received | | |
| Total Queries Forwarded | | |
| Total Queries Answered | | |
| Per Query Cost | | |
| Per Node Cost | | |

---

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `register` | Join the network |
| `search` | Search for one file |
| `run-queries` | Run all queries automatically |
| `files` | Show my files |
| `neighbors` | Show routing table |
| `stats` | Show performance stats |
| `download <ip> <port> <file>` | Download a file |
| `leave` | Gracefully exit |
| `exit` | Force quit |

---

## Verify Protocol Compliance (Section 4.1)

### Test Bootstrap Server with netcat (Optional Verification)

**macOS/Linux:**
```bash
# Open terminal
nc -u 127.0.0.1 5000

# Type and press Enter:
0036 REG 127.0.0.1 5001 testuser

# Expected response:
0014 REGOK 0
# (or REGOK with node list if others registered)

# Unregister:
0040 UNREG 127.0.0.1 5001 testuser

# Expected response:
0012 UNROK 0
```

**Windows:** Use a UDP client tool or test directly with Python scripts

### Message Format Verification

All messages should follow:
- **4-digit length prefix** (includes the 4 digits itself)
- **Space after length**
- **Command in UPPERCASE**
- **Space-separated parameters**

**Example:**
- `0036 REG 127.0.0.1 5001 node1` ← Length is 36 (4 digits + space + 31 chars)

### Protocol Compliance Checklist

- [ ] REG message format: `length REG IP port username`
- [ ] REGOK message format: `length REGOK no_nodes [IP port]*`
- [ ] UNREG message format: `length UNREG IP port username`
- [ ] UNROK message format: `length UNROK value`
- [ ] JOIN message format: `length JOIN IP port`
- [ ] JOINOK message format: `length JOINOK value`
- [ ] LEAVE message format: `length LEAVE IP port`
- [ ] LEAVEOK message format: `length LEAVEOK value`
- [ ] SER message format: `length SER IP port "filename" hops`
- [ ] SEROK message format: `length SEROK no_files IP port hops filename1 ...`
- [ ] All messages use UDP (except Bootstrap which uses TCP)
- [ ] Length prefix is exactly 4 digits
- [ ] Commands are in UPPERCASE

---

## Troubleshooting

### Node won't register

**Windows:**
```cmd
REM Check bootstrap server is running
netstat -an | findstr 5000
```

**macOS/Linux:**
```bash
# Check bootstrap server is running
netstat -an | grep 5000
```

### "Already registered" error
```bash
# In the node:
> leave
> exit

# Restart the node with different username or port
```

### Can't find file
```bash
# Remember: Search uses word boundaries
# "Lord" matches "Lord of the rings" ✓
# "Lo" does NOT match "Lord of the rings" ✗
```

### No neighbors showing
```bash
# Make sure you ran: register
# Wait 2-3 seconds after registration
# Check: neighbors
```

---

## Expected Results (Based on Section 4.1 Protocol)

### Bootstrap Server Communication
- **REG format:** `length REG IP_address port_no username`
- **REGOK responses:**
  - 0 = Success, no other nodes
  - 1-2 = Success, returning 1-2 node contacts
  - 9998 = Already registered (must UNREG first)
  - 9999 = Command error
- **UNREG format:** `length UNREG IP_address port_no username`
- **UNROK responses:**
  - 0 = Success
  - 9999 = Error (not in registry or bad command)

### Network Stats (10 nodes)
- **Neighbors per node:** 2 (as per BS, but may grow to 3-4)
- **Network diameter:** 3-5 hops
- **Total messages:** 500-1500 (depends on flooding)
- **Routing table size:** 2-4 neighbors

### Query Performance  
- **Success rate:** 85-95%
- **Average hops:** 2-3
- **Average latency:** 20-80ms
- **Messages per query:** 8-15 (flooding overhead)
- **Word-boundary matching:** "Lord" matches "Lord of the rings" ✓, but NOT "Lo Game" ✗

### After Node Removal (8 nodes)
- **Success rate:** 75-90% (slight decrease expected)
- **Average hops:** 2-4 (may increase slightly)
- **Messages per query:** 6-12 (fewer nodes = fewer messages)
- **Network connectivity:** Should remain functional
- **Routing tables:** Updated automatically via LEAVE messages

---

## Phase 4 Requirements Checklist

**Before starting:**
- [ ] Bootstrap server starts without errors
- [ ] All 10 nodes start and register successfully
- [ ] Each node shows 3-5 files
- [ ] Each node shows 2+ neighbors (routing table)

**Experiment 1 (10 nodes):**
- [ ] Select 3 random nodes for queries
- [ ] Run all queries from queries.txt on each selected node
- [ ] Collect statistics from ALL 10 nodes (not just query nodes)
- [ ] Record: queries received, forwarded, answered by EACH node
- [ ] Record: routing table size for EACH node
- [ ] Record: hops and latency for EACH query
- [ ] Calculate: min, max, avg, stddev for hops
- [ ] Calculate: min, max, avg, stddev for latency
- [ ] Calculate: min, max, avg, stddev for messages per node
- [ ] Calculate: min, max, avg, stddev for node degree

**Node Removal:**
- [ ] Remove first node gracefully using LEAVE command
- [ ] Wait for network stabilization (5 seconds)
- [ ] Verify node removed from all routing tables
- [ ] Remove second node gracefully using LEAVE command
- [ ] Wait for network stabilization (5 seconds)
- [ ] Verify both nodes unregistered from Bootstrap Server

**Experiment 2 (8 nodes):**
- [ ] Use SAME 3 query nodes from Experiment 1 (if still alive)
- [ ] Run all queries again from queries.txt
- [ ] Collect statistics from ALL remaining 8 nodes
- [ ] Record same metrics as Experiment 1
- [ ] Calculate same statistics as Experiment 1

**Analysis:**
- [ ] Plot CDF of hops (both experiments)
- [ ] Plot CDF of latency (both experiments)
- [ ] Plot CDF of messages per node (both experiments)
- [ ] Plot CDF of node degree (both experiments)
- [ ] Calculate per-query cost for both experiments
- [ ] Calculate per-node cost for both experiments
- [ ] Compare Experiment 1 vs Experiment 2 results

**Report Requirements:**
- [ ] Include all min/max/avg/stddev calculations
- [ ] Include all 4 CDF plots (or 8 if separate per experiment)
- [ ] Discuss query success rates
- [ ] Discuss impact of node removal on performance
- [ ] Analyze Q >> N and N >> Q scenarios
- [ ] Suggest improvements for reducing hops/latency/messages
- [ ] Report must not exceed 5 pages

**Demo Preparation:**
- [ ] Search works with complete file names
- [ ] Search works with partial file names (word boundaries)
- [ ] File download works (TCP/REST API)
- [ ] File integrity verified (SHA-256 hash)
- [ ] System continues operating after node failures
- [ ] All group members present
- [ ] 15-min demo + 5-min viva ready

---

## Demo Script (15 min)

**Minute 0-2:** Setup
- Show bootstrap + 10 nodes running
- Show registration messages

**Minute 2-3:** File Display
- Show `files` on 2-3 nodes
- Show different file distributions

**Minute 3-8:** Search Demo
- Search "Twilight" (full match)
- Search "Happy" (partial match)
- Search "Baby" (multiple results)
- Show hop counts and latency

**Minute 8-11:** File Transfer
- Download "Twilight" from found node
- Show file size (MB)
- Show hash values
- Show integrity verification

**Minute 11-14:** Failure Recovery
- Remove 2 nodes with `leave`
- Show routing tables updated
- Repeat search - still works!

**Minute 14-15:** Statistics
- Show `stats` output
- Mention analysis done (CDF plots)
- Q&A buffer

---

## You're Ready!

Everything is set up and verified. Just follow these steps and you'll have successful Phase 4 results.

**Good luck with your testing and demo!**

---

*Last Updated: November 29, 2025*
*All fixes verified and tested ✅*
