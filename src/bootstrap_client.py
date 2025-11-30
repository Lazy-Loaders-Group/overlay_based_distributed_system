"""
Bootstrap server client for node registration.
"""

import socket
import random
from protocol import MessageFormatter, MessageParser


class BootstrapClient:
    """Handles communication with bootstrap server."""
    
    def __init__(self, bs_ip, bs_port):
        self.bs_ip = bs_ip
        self.bs_port = bs_port
        self.buffer_size = 4096
    
    def register(self, my_ip, my_port, username):
        """
        Register node with bootstrap server.
        
        Args:
            my_ip (str): This node's IP
            my_port (int): This node's port
            username (str): Unique username
            
        Returns:
            list: List of existing nodes [{'ip': str, 'port': int}, ...]
        """
        try:
            # Create message
            message = MessageFormatter.create_reg_message(my_ip, my_port, username)
            
            # Connect to bootstrap server (using TCP based on provided code)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.bs_ip, self.bs_port))
            
            # Send registration
            sock.send(message.encode('utf-8'))
            
            # Receive response
            data = sock.recv(self.buffer_size)
            sock.close()
            
            # Parse response
            tokens = MessageFormatter.parse_message(data)
            result = MessageParser.parse_regok(tokens)
            
            if result is None:
                print(f"[ERROR] Invalid REGOK response: {data}")
                return []
            
            status = result['status']
            nodes = result['nodes']
            
            if status == 0:
                print("[BOOTSTRAP] Registered successfully. No other nodes in system.")
                return []
            elif status > 0 and status < 9000:
                print(f"[BOOTSTRAP] Registered successfully. Received {len(nodes)} node(s).")
                # Return only first 2 nodes (or all if less than 2), but randomly selected
                if len(nodes) > 2:
                    selected = random.sample(nodes, 2)
                    return selected
                return nodes
            elif status == 9998:
                print("[ERROR] Already registered. Please unregister first.")
                return None
            elif status == 9999:
                print("[ERROR] Registration failed. Command error.")
                return None
            else:
                print(f"[ERROR] Registration failed with code: {status}")
                return None
                
        except socket.timeout:
            print("[ERROR] Bootstrap server connection timeout")
            return None
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            return None
    
    def unregister(self, my_ip, my_port, username):
        """
        Unregister node from bootstrap server.
        
        Args:
            my_ip (str): This node's IP
            my_port (int): This node's port
            username (str): Username used during registration
            
        Returns:
            bool: True if successful
        """
        try:
            # Create message
            message = MessageFormatter.create_unreg_message(my_ip, my_port, username)
            
            # Connect to bootstrap server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.bs_ip, self.bs_port))
            
            # Send unregistration
            sock.send(message.encode('utf-8'))
            
            # Receive response
            data = sock.recv(self.buffer_size)
            sock.close()
            
            # Parse response
            tokens = MessageFormatter.parse_message(data)
            
            if len(tokens) >= 2 and tokens[0] == 'UNROK':
                value = int(tokens[1])
                if value == 0:
                    print("[BOOTSTRAP] Unregistered successfully.")
                    return True
                else:
                    print(f"[ERROR] Unregistration failed with code: {value}")
                    return False
            else:
                print(f"[ERROR] Invalid UNROK response: {data}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Unregistration failed: {e}")
            return False
