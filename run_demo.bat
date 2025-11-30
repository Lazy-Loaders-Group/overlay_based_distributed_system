@echo off
REM Windows Batch Script for Distributed Content Searching System Demo

echo Starting Distributed Content Searching System Demo...

REM Create logs directory
if not exist logs mkdir logs

REM Start Bootstrap Server
echo Starting Bootstrap Server...
start "Bootstrap Server" cmd /k "python src\bootstrap_server.py 5555 > logs\bs.log 2>&1"
timeout /t 2 /nobreak >nul

REM Start Nodes
echo Starting Nodes...

REM Node 1
start "Node 1" cmd /k "python src\node.py --port 5001 --username node1 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs\node1.log 2>&1"
echo Started Node 1 (Port 5001)
timeout /t 1 /nobreak >nul

REM Node 2
start "Node 2" cmd /k "python src\node.py --port 5002 --username node2 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs\node2.log 2>&1"
echo Started Node 2 (Port 5002)
timeout /t 1 /nobreak >nul

REM Node 3
start "Node 3" cmd /k "python src\node.py --port 5003 --username node3 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs\node3.log 2>&1"
echo Started Node 3 (Port 5003)
timeout /t 1 /nobreak >nul

REM Node 4
start "Node 4" cmd /k "python src\node.py --port 5004 --username node4 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs\node4.log 2>&1"
echo Started Node 4 (Port 5004)
timeout /t 1 /nobreak >nul

REM Node 5
start "Node 5" cmd /k "python src\node.py --port 5005 --username node5 --bs-ip 127.0.0.1 --bs-port 5555 --auto-register > logs\node5.log 2>&1"
echo Started Node 5 (Port 5005)

echo.
echo All background systems running!
echo ---------------------------------------------------
echo To interact with the system:
echo 1. Open a NEW Command Prompt window.
echo 2. Run the following command to start your interactive node:
echo    python src\node.py --port 5006 --username my_node --bs-ip 127.0.0.1 --bs-port 5555
echo.
echo 3. In your new node, type 'register' to join.
echo 4. Type 'search ^<filename^>' to find files.
echo 5. Type 'download ^<ip^> ^<port^> ^<filename^>' to download.
echo ---------------------------------------------------
echo Logs are being written to logs\ directory.
echo Close the individual command windows to stop the network.
echo.

pause
