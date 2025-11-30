import hashlib
import random
import os

class FileManager:
    """Handles file generation, storage, and hashing."""
    
    def __init__(self):
        self.file_cache = {}  # filename -> bytes
        self.hashes = {}      # filename -> hash
    
    def get_file_content(self, filename):
        """
        Get file content. Generates it if not present.
        
        Args:
            filename (str): Name of the file.
            
        Returns:
            bytes: File content.
        """
        if filename not in self.file_cache:
            self._generate_file(filename)
        
        return self.file_cache[filename]
    
    def get_file_hash(self, filename):
        """Get SHA256 hash of a file."""
        if filename not in self.hashes:
            if filename in self.file_cache:
                self.hashes[filename] = self._calculate_hash(self.file_cache[filename])
            else:
                self._generate_file(filename)
        
        return self.hashes[filename]
    
    def _generate_file(self, filename):
        """Generate random file content between 2-10 MB."""
        # Size in bytes (2MB to 10MB)
        size = random.randint(2 * 1024 * 1024, 10 * 1024 * 1024)
        
        # Generate random bytes
        # Using os.urandom might be slow for 10MB, let's use a faster way or just random bytes
        # For simulation, repeating a small pattern is faster but less "random".
        # Let's use random.getrandbits for a seed and generate.
        # Actually, os.urandom is fine for 10MB.
        content = os.urandom(size)
        
        self.file_cache[filename] = content
        self.hashes[filename] = self._calculate_hash(content)
        
        print(f"[FILE] Generated '{filename}': {size/1024/1024:.2f} MB, Hash: {self.hashes[filename]}")

    def _calculate_hash(self, data):
        """Calculate SHA256 hash of data."""
        return hashlib.sha256(data).hexdigest()
