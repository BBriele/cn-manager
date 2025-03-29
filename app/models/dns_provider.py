import importlib.util
from datetime import datetime
from models.base_model import BaseModel
import json
from abc import ABC, abstractmethod

# ==========================
# 🔹 Interfaccia per i provider DNS
# ==========================
class DNSProvider(ABC):
    """
    Abstract Base Class for DNS Providers.
    All specific providers must implement these methods.
    """

    def __init__(self, config_data):
        self.config_data = config_data

    @abstractmethod
    def create_record(self, domain, record_type, value):
        pass

    @abstractmethod
    def delete_record(self, domain, record_type, value):
        pass

    @abstractmethod
    def get_records(self, domain):
        pass

    @abstractmethod
    def update_record(self, domain, record_type, old_value, new_value):
        pass

    @abstractmethod
    def perform_dns_challenge(self, domain, challenge_value):
        """
        Method to handle the DNS-01 challenge for SSL certificate generation.
        """
        pass
