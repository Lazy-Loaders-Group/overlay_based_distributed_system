#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping all nodes and server..."
    pkill -f "src/node.py"
    pkill -f "src/bootstrap_server.py"
    exit
}

trap cleanup SIGINT

echo "Starting Distributed Content Searching System Demo..."

# Create logs directory
mkdir -p logs

# Start Bootstrap Server
echo "Starting Bootstrap Server..."
python3 src/bootstrap_server.py 5555 > logs/bs.log 2>&1 &
BS_PID=$!
sleep 2

# Start Nodes
echo "Starting Nodes..."
# Node 1
python3 src/node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs/node1.log 2>&1 &
echo "Started Node 1 (Port 5001)"
sleep 1

# Node 2
python3 src/node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs/node2.log 2>&1 &
echo "Started Node 2 (Port 5002)"
sleep 1

# Node 3
python3 src/node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs/node3.log 2>&1 &
echo "Started Node 3 (Port 5003)"
sleep 1

# Node 4
python3 src/node.py --port 5004 --username node4 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs/node4.log 2>&1 &
echo "Started Node 4 (Port 5004)"
sleep 1

# Node 5
python3 src/node.py --port 5005 --username node5 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs/node5.log 2>&1 &
echo "Started Node 5 (Port 5005)"

echo ""
echo "All background systems running!"
echo "---------------------------------------------------"
echo "To interact with the system:"
echo "1. Open a NEW terminal window."
echo "2. Run the following command to start your interactive node:"
echo "   python3 src/node.py --port 5006 --username my_node --bs-ip 127.0.0.1 --bs-port 5555"
echo ""
echo "3. In your new node, type 'register' to join."
echo "4. Type 'search <filename>' to find files."
echo "5. Type 'download <ip> <port> <filename>' to download."
echo "---------------------------------------------------"
echo "Logs are being written to logs/ directory."
echo "Press Ctrl+C in THIS terminal to stop the background network."

# Keep script running
wait
