import socket
from bootstrap_manager import Node
from random import shuffle
import threading
import random
import sys

class BootstrapServer:
    """Bootstrap server for managing node registration."""
    def __init__(self, port=55000):
        self.port = port
        self.nodes = []  # List of {'ip': ip, 'port': port, 'username': username}
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        """Start the bootstrap server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(5)
        print(f"[BOOTSTRAP] Server started on port {self.port}")

        while self.running:
            try:
                client_sock, addr = self.sock.accept()
                threading.Thread(target=self.handle_client, args=(client_sock,), daemon=True).start()
            except Exception as e:
                if self.running:
                    print(f"[ERROR] Accept error: {e}")

    def handle_client(self, client_sock):
        """Handle client connections."""
        try:
            data = client_sock.recv(1024).decode('utf-8')
            if not data:
                return

            response = self.process_message(data)
            client_sock.send(response.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Client handling error: {e}")
        finally:
            client_sock.close()

    def process_message(self, message):
        """Process incoming message."""
        parts = message.split()
        if len(parts) < 2:
            return self.format_error()

        command = parts[1]
        
        if command == 'REG':
            return self.handle_reg(parts)
        elif command == 'UNREG':
            return self.handle_unreg(parts)
        else:
            return self.format_error()

    def handle_reg(self, parts):
        """Handle node registration."""
        # Format: length REG IP_address port_no username
        if len(parts) < 5:
            return self.format_error()

        ip = parts[2]
        port = int(parts[3])
        username = parts[4]

        with self.lock:
            # Check if already registered
            for node in self.nodes:
                if node['port'] == port and node['username'] == username:
                     if node['ip'] == ip:
                         return self.format_response(f"REGOK 9998")
            
            # Select random nodes to return
            neighbors = []
            if self.nodes:
                # Return up to 2 random nodes
                candidates = [n for n in self.nodes if not (n['ip'] == ip and n['port'] == port)]
                if len(candidates) > 2:
                    neighbors = random.sample(candidates, 2)
                else:
                    neighbors = candidates

            # Register new node
            self.nodes.append({'ip': ip, 'port': port, 'username': username})
            print(f"[BOOTSTRAP] Registered: {username} at {ip}:{port}")

            # Construct response
            # length REGOK no_nodes IP_1 port_1 IP_2 port_2
            response = f"REGOK {len(neighbors)}"
            for neighbor in neighbors:
                response += f" {neighbor['ip']} {neighbor['port']}"
            
            return self.format_response(response)

    def handle_unreg(self, parts):
        """Handle node unregistration."""
        # Format: length UNREG IP_address port_no username
        if len(parts) < 5:
            return self.format_error()

        ip = parts[2]
        port = int(parts[3])
        username = parts[4]

        with self.lock:
            # Find and remove node
            for i, node in enumerate(self.nodes):
                if node['ip'] == ip and node['port'] == port and node['username'] == username:
                    del self.nodes[i]
                    print(f"[BOOTSTRAP] Unregistered: {username}")
                    return self.format_response("UNROK 0")
            
            return self.format_response("UNROK 9999")

    def format_response(self, content):
        """Format response with length prefix."""
        # Add length prefix
        content = " " + content
        length = len(content) + 4
        return f"{length:04d}{content}"

    def format_error(self):
        """Format error message."""
        return self.format_response("ERROR")


class BootstrapServerConnection:
    def __init__(self, bs, me):
        self.bs = bs
        self.me = me
        self.users = []

    def __enter__(self):
        self.users = self.connect_to_bs()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.unreg_from_bs()

    def message_with_length(self, message):
        '''
        Helper function to prepend the length of the message to the message itself
        Args:
            message (str): message to prepend the length
        Returns:
            str: Prepended message
        '''
        message = " " + message
        message = str((10000+len(message)+5))[1:] + message
        return message

    def connect_to_bs(self):
        '''
        Register node at bootstrap server.
        Args:
            bs (Node): Bootstrap server node
            me (Node): This node
        Returns:
            list(Node) : List of other nodes in the distributed system
        Raises:
            RuntimeError: If server sends an invalid response or if registration is unsuccessful
        '''
        self.unreg_from_bs()
        buffer_size = 1024
        message = "REG "+ self.me.ip + " " +str(self.me.port) +" " + self.me.name

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.bs.ip, self.bs.port))
        s.send(self.message_with_length(message))
        data = s.recv(buffer_size)
        s.close()
        print(data)
        
        toks = data.split()
        
        if (len(toks) < 3):
            raise RuntimeError("Invalid message")
        
        if (toks[1] != "REGOK"):
            raise RuntimeError("Registration failed")
        
        num = int(toks[2])
        if (num < 0):
            raise RuntimeError("Registration failed")
            
        if (num == 0):
            return []
        elif (num == 1):
            return [Node(toks[3], int(toks[4]), toks[5])]
        else:
            l = range(1, num+1)
            shuffle(l)
            return [Node(toks[l[0]*3], int(toks[l[0]*3+1]), toks[l[0]*3+2]), Node(toks[l[1]*3], int(toks[l[1]*3+1]), toks[l[1]*3+2])]
        
    def unreg_from_bs(self):
        '''
        Unregister node at bootstrap server.
        Args:
            bs (tuple(str, int)): Bootstrap server IP address and port as a tuple.
            me (tuple(str, int)): This node's IP address and port as a tuple.
            myname (str)        : This node's name
        Returns:
            list(tuple(str, int)) : List of other nodes in the distributed system
        Raises:
            RuntimeError: If unregistration is unsuccessful
        '''
        buffer_size = 1024
        message = "UNREG "+ self.me.ip + " " +str(self.me.port) +" " + self.me.name

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.bs.ip, self.bs.port))
        s.send(self.message_with_length(message))
        data = s.recv(buffer_size)
        s.close()
        
        toks = data.split()
        if (toks[1] != "UNROK"):
            raise RuntimeError("Unreg failed")


if __name__ == '__main__':
    """Run the bootstrap server."""
    print("=" * 60)
    print("BOOTSTRAP SERVER - Distributed File Search System")
    print("=" * 60)
    print("Starting bootstrap server on port 55000...")
    print("This server helps nodes find each other.")
    print("Keep this terminal open while running your demo.")
    print("=" * 60)
    print()
    
    server = BootstrapServer(port=55000)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[BOOTSTRAP] Shutting down...")
        server.running = False

