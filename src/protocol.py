"""
Protocol handler for distributed content searching system.
Handles message formatting, parsing, and protocol specifications.
"""

class MessageFormatter:
    """Handles message formatting with length prefix as per protocol specification."""
    
    @staticmethod
    def format_message(message):
        """
        Format message with 4-digit length prefix.
        
        Args:
            message (str): Message to format
            
        Returns:
            str: Formatted message with length prefix
        """
        # Add space and calculate total length including the 4-digit prefix
        full_message = " " + message
        length = len(full_message) + 4
        return f"{length:04d}{full_message}"
    
    @staticmethod
    def parse_message(data):
        """
        Parse received message.
        
        Args:
            data (bytes or str): Raw message data
            
        Returns:
            list: Tokenized message components
        """
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        
        # Remove length prefix and split
        if len(data) >= 5:
            message = data[5:]  # Skip "0000 " prefix
            return message.split()
        return []
    
    @staticmethod
    def create_reg_message(ip, port, username):
        """Create REG message for bootstrap server."""
        message = f"REG {ip} {port} {username}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_unreg_message(ip, port, username):
        """Create UNREG message for bootstrap server."""
        message = f"UNREG {ip} {port} {username}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_join_message(ip, port):
        """Create JOIN message for other nodes."""
        message = f"JOIN {ip} {port}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_joinok_message(value=0):
        """Create JOINOK response."""
        message = f"JOINOK {value}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_leave_message(ip, port):
        """Create LEAVE message."""
        message = f"LEAVE {ip} {port}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_leaveok_message(value=0):
        """Create LEAVEOK response."""
        message = f"LEAVEOK {value}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_ser_message(ip, port, filename, hops=0):
        """Create SER (search) message."""
        message = f'SER {ip} {port} "{filename}" {hops}'
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_serok_message(num_files, ip, port, hops, filenames):
        """Create SEROK (search response) message."""
        files_str = " ".join(filenames)
        message = f"SEROK {num_files} {ip} {port} {hops} {files_str}"
        return MessageFormatter.format_message(message)
    
    @staticmethod
    def create_error_message():
        """Create ERROR message."""
        return MessageFormatter.format_message("ERROR")


class MessageParser:
    """Parse incoming messages and extract relevant information."""
    
    @staticmethod
    def parse_regok(tokens):
        """
        Parse REGOK response from bootstrap server.
        
        Returns:
            dict: {'status': int, 'nodes': [{'ip': str, 'port': int}, ...]}
        """
        if len(tokens) < 2 or tokens[0] != 'REGOK':
            return None
        
        num_nodes = int(tokens[1])
        nodes = []
        
        if num_nodes > 0 and len(tokens) >= 4:
            # Parse node entries (IP port pairs)
            for i in range(2, len(tokens) - 1, 2):
                if i + 1 < len(tokens):
                    nodes.append({
                        'ip': tokens[i],
                        'port': int(tokens[i + 1])
                    })
        
        return {
            'status': num_nodes,
            'nodes': nodes
        }
    
    @staticmethod
    def parse_join(tokens):
        """Parse JOIN message."""
        if len(tokens) >= 3 and tokens[0] == 'JOIN':
            return {
                'ip': tokens[1],
                'port': int(tokens[2])
            }
        return None
    
    @staticmethod
    def parse_leave(tokens):
        """Parse LEAVE message."""
        if len(tokens) >= 3 and tokens[0] == 'LEAVE':
            return {
                'ip': tokens[1],
                'port': int(tokens[2])
            }
        return None
    
    @staticmethod
    def parse_ser(tokens):
        """Parse SER (search) message."""
        if len(tokens) >= 4 and tokens[0] == 'SER':
            # Extract filename (may be quoted)
            filename_start = 3
            hops_idx = len(tokens) - 1
            
            # Join filename parts (handle spaces in filename)
            filename_parts = tokens[filename_start:hops_idx]
            filename = " ".join(filename_parts).strip('"')
            
            return {
                'ip': tokens[1],
                'port': int(tokens[2]),
                'filename': filename,
                'hops': int(tokens[hops_idx])
            }
        return None
    
    @staticmethod
    def parse_serok(tokens):
        """Parse SEROK (search response) message."""
        if len(tokens) >= 5 and tokens[0] == 'SEROK':
            num_files = int(tokens[1])
            ip = tokens[2]
            port = int(tokens[3])
            hops = int(tokens[4])
            filenames = tokens[5:] if num_files > 0 else []
            
            return {
                'num_files': num_files,
                'ip': ip,
                'port': port,
                'hops': hops,
                'filenames': filenames
            }
        return None
