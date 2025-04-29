import uuid
from datetime import datetime
from typing import List, Optional
from models.base_model import BaseModel
#from models.domain import Domain
#from models.cloudflare import CloudflareConfig
from models.dns_config import DNSConfig

class Certificate(BaseModel):
    model_name = "certificates"  # Define the model name
    schema = {
        **BaseModel.schema,
        'email': {'type': str, 'required': True},
        'name': {'type': str, 'required': True},
        'domains': {'type': list, 'required': True},
        'dns_challenge': {'type': bool, 'required': True},
        'dns_config': {'type': (DNSConfig, type(None))},
        'agree': {'type': bool, 'required': True},
        'certificate_path': {'type': (str, type(None))},
        'private_key_path': {'type': (str, type(None))}
    }

    def __init__(self, **kwargs):
        """
        Initialize the Certificate model, calling the parent constructor.
        """
        super().__init__(**kwargs)
        
    def get_domain_names(self) -> List[str]:
        return [domain.name if isinstance(domain, BaseModel) else domain for domain in self.domains]

    def get_email(self) -> str:
        return self.email

    def set_email(self, email: str):
        self.email = email
        self.updated_at = datetime.utcnow()

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name
        self.updated_at = datetime.utcnow()

    def get_domains(self) -> List[object]:
        return self.domains

    def set_domains(self, domains: List[object]):
        self.domains = domains
        self.updated_at = datetime.utcnow()

    def get_dns_challenge(self) -> bool:
        return self.dns_challenge

    def set_dns_challenge(self, dns_challenge: bool):
        self.dns_challenge = dns_challenge
        self.updated_at = datetime.utcnow()

    def get_dns_config(self) -> Optional[object]:
        return self.dns_config

    def set_dns_config(self, dns_config: Optional[object]):
        self.dns_config = dns_config
        self.updated_at = datetime.utcnow()

    def get_agree(self) -> bool:
        return self.agree

    def set_agree(self, agree: bool):
        self.agree = agree
        self.updated_at = datetime.utcnow()

    def get_certificate_path(self) -> Optional[str]:
        return self.certificate_path

    def set_certificate_path(self, certificate_path: Optional[str]):
        self.certificate_path = certificate_path
        self.updated_at = datetime.utcnow()

    def get_private_key_path(self) -> Optional[str]:
        return self.private_key_path

    def set_private_key_path(self, private_key_path: Optional[str]):
        self.private_key_path = private_key_path
        self.updated_at = datetime.utcnow()

    @classmethod
    def get_by_email(cls, items, email):
        """
        Specific method to get certificates by email.
        """
        return cls.get_by(items, 'email', email)
