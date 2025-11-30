import socket
import threading
import random
import sys

class BootstrapServer:
    def __init__(self, port=5000):
        self.port = port
        self.nodes = []  # List of {'ip': ip, 'port': port, 'username': username}
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        # Format: length REG IP_address port_no username
        if len(parts) < 5:
            return self.format_error()

        ip = parts[2]
        port = int(parts[3])
        username = parts[4]

        with self.lock:
            # Check if already registered
            for node in self.nodes:
                if node['port'] == port and node['username'] == username: # Simple check, IP might be same for local test
                     # In a real scenario, we check IP too. For local test, IP is often 127.0.0.1
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
        # Add length prefix
        content = " " + content
        length = len(content) + 4
        return f"{length:04d}{content}"

    def format_error(self):
        return self.format_response("ERROR")

if __name__ == "__main__":
    server = BootstrapServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[BOOTSTRAP] Stopping server...")
