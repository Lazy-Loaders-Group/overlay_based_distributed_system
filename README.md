# Distributed Content Searching System

A distributed peer-to-peer (P2P) system implementation that allows nodes to join a network, search for files using a flooding algorithm, and download them reliably using a REST API.

## 🚀 Features

- **Distributed Network**: Nodes form an unstructured overlay network.
- **File Search**: UDP-based flooding algorithm to find files across nodes.
- **File Transfer**: Reliable file download using HTTP REST API (Flask).
- **Resilience**: Handles node failures and graceful departures.
- **Performance Analysis**: Built-in tools to measure latency, hops, and message overhead.

## 📋 Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)

## 🛠️ Installation

1. **Clone or Extract the Project**
   Navigate to the project directory.

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Quick Start (Recommended)

We provide a demo script that sets up a local network with a Bootstrap Server and 5 nodes automatically.

1. **Make the script executable** (Mac/Linux):
   ```bash
   chmod +x run_demo.sh
   ```

2. **Run the Demo Network**:
   ```bash
   ./run_demo.sh
   ```
   *This starts the Bootstrap Server and 5 background nodes.*

3. **Join the Network**:
   Open a **NEW** terminal window and run your own interactive node:
   ```bash
   python3 src/node.py --port 5006 --username my_node --bs-ip 127.0.0.1 --bs-port 5000
   ```

4. **Interact**:
   Inside your node's terminal, try these commands:
   - `register` : Join the network.
   - `search <filename>` : Search for a file (e.g., `search lord`, `search baby`).
   - `download <ip> <port> <filename>` : Download a file found in search results.
   - `stats` : View performance statistics.
   - `leave` : Leave the network.

5. **Stop**:
   Press `Ctrl+C` in the terminal running `./run_demo.sh` to stop the entire network.

## 🔧 Manual Setup

If you prefer to run components individually:

1. **Start Bootstrap Server**:
   ```bash
   python3 src/bootstrap_server.py
   ```

2. **Start Nodes**:
   Open multiple terminals and run a node in each (change ports for each node):
   ```bash
   # Node 1
   python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5000

   # Node 2
   python3 src/node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5000
   ```

## 🎮 CLI Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `register` | Register with BS and join network | `register` |
| `search` | Search for a file | `search <filename>` |
| `download` | Download a file from a node | `download <ip> <port> <filename>` |
| `files` | List files hosted by this node | `files` |
| `neighbors` | Show connected neighbors | `neighbors` |
| `stats` | Show node statistics | `stats` |
| `leave` | Gracefully leave the network | `leave` |
| `exit` | Stop the node and exit | `exit` |

## 📊 Performance Analysis

The system automatically logs performance metrics to the `logs/` directory.

To generate performance graphs (CDF of Latency, Hops, Messages):
```bash
python3 src/plot_stats.py
```
This will generate `.png` plots in the project root.

## 📂 Project Structure

```
├── src/
│   ├── node.py              # Main node logic (UDP + REST API)
│   ├── bootstrap_server.py  # Local Bootstrap Server for testing
│   ├── bootstrap_client.py  # Client to talk to BS
│   ├── search_engine.py     # Search logic (flooding)
│   ├── file_manager.py      # File generation & hashing
│   ├── protocol.py          # Message parsing/formatting
│   ├── routing_table.py     # Neighbor management
│   ├── statistics.py        # Metrics collection
│   └── plot_stats.py        # Graph generation script
├── logs/                    # Log files (auto-generated)
├── file_names.txt           # Pool of file names
├── queries.txt              # Sample queries
├── requirements.txt         # Python dependencies
├── run_demo.sh              # Quick start script
└── README.md                # This file
```
