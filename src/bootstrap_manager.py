import socket
import random

class Node:
    def __init__(self, ip, port, username=""):
        self.ip = ip
        self.port = port
        self.username = username
        
    def __repr__(self):
        return f"{self.ip}:{self.port}"

class BootstrapManager:
    def __init__(self, bs_ip, bs_port, my_ip, my_port, my_username):
        self.bs_ip = bs_ip
        self.bs_port = bs_port
        self.me = Node(my_ip, my_port, my_username)
        
    def message_with_length(self, message):
        '''
        Prepend length to message.
        Length = 4 digits + length of message (including spaces).
        '''
        # Add space separator
        full_msg = " " + message
        # Calculate total length: 4 digits + len(full_msg)
        length = 4 + len(full_msg)
        return f"{length:04d}{full_msg}"

    def connect_to_bs(self):
        '''
        Register node at bootstrap server.
        Returns:
            list(Node) : List of other nodes
        '''
        # Unregister first to be safe (as per project description suggestion)
        # But maybe we should just register. The provided code did unreg first.
        # self.unreg_from_bs() 
        
        buffer_size = 1024
        message = f"REG {self.me.ip} {self.me.port} {self.me.username}"
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.bs_ip, self.bs_port))
            s.send(self.message_with_length(message).encode('utf-8'))
            data = s.recv(buffer_size).decode('utf-8')
            s.close()
            
            print(f"[BOOTSTRAP] Response: {data}")
            
            toks = data.split()
            
            if len(toks) < 3:
                print("Invalid message")
                return []
            
            if toks[1] != "REGOK":
                print(f"Registration failed: {toks[1]}")
                return []
            
            num = int(toks[2])
            
            if num == 0:
                return []
            elif num == 1:
                # Expecting: length REGOK 1 IP1 Port1
                if len(toks) >= 5:
                    return [Node(toks[3], int(toks[4]))]
            else:
                # Expecting: length REGOK N IP1 Port1 IP2 Port2 ...
                # We need to parse all of them and pick 2 random ones?
                # The project description says:
                # "BS will actually return all the nodes known to it. However, you should use only the first 2 nodes to connect."
                # Wait, "use only the first 2 nodes".
                # The provided code shuffled them.
                # Let's parse all available nodes first.
                
                nodes = []
                # Stride is 2: IP, Port
                # Start index 3
                for i in range(3, len(toks)-1, 2):
                    nodes.append(Node(toks[i], int(toks[i+1])))
                
                # The provided code shuffled and returned 2.
                # Project guide says "use only the first 2 nodes to connect" (line 106).
                # But line 22 says "4th node ... should join only to 2 randomly selected nodes from the list".
                # So shuffling is good.
                
                if len(nodes) > 2:
                    random.shuffle(nodes)
                    return nodes[:2]
                return nodes
                
        except Exception as e:
            print(f"[ERROR] Bootstrap connection failed: {e}")
            return []
            
    def unreg_from_bs(self):
        '''
        Unregister node at bootstrap server.
        '''
        buffer_size = 1024
        message = f"UNREG {self.me.ip} {self.me.port} {self.me.username}"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.bs_ip, self.bs_port))
            s.send(self.message_with_length(message).encode('utf-8'))
            data = s.recv(buffer_size).decode('utf-8')
            s.close()
            
            toks = data.split()
            if len(toks) > 1 and toks[1] == "UNROK":
                return True
            return False
        except Exception as e:
            print(f"[ERROR] Bootstrap unreg failed: {e}")
            return False
