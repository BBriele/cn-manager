import json
import os
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from .models import ProxyConfig, SSLCertificate

class JsonDatabase:
    """JSON file-based database implementation"""
    
    def __init__(self, storage_path: str = "data/storage"):
        """
        Initialize database with storage paths
        
        Args:
            storage_path: Base path for JSON storage files
        """
        self.storage_path = storage_path
        self.proxies_file = os.path.join(storage_path, "proxies.json")
        self.certs_file = os.path.join(storage_path, "certificates.json")
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage directory and files if they don't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Initialize empty JSON files if they don't exist
        for file_path in [self.proxies_file, self.certs_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)

    def _load_json(self, file_path: str) -> List[Dict]:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_json(self, file_path: str, data: List[Dict]):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def get_proxies(self) -> List[ProxyConfig]:
        """Get all proxy configurations"""
        data = self._load_json(self.proxies_file)
        return [ProxyConfig(**item) for item in data]

    def add_proxy(self, proxy: ProxyConfig) -> str:
        """
        Add new proxy configuration
        
        Args:
            proxy: ProxyConfig object to add
            
        Returns:
            str: Generated proxy ID
        """
        proxies = self._load_json(self.proxies_file)
        
        # Generate new ID and timestamps
        proxy_dict = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            **proxy.__dict__
        }
        
        proxies.append(proxy_dict)
        self._save_json(self.proxies_file, proxies)
        return proxy_dict["id"]