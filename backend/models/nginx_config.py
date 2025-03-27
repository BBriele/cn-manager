import uuid
from datetime import datetime
from typing import List, Optional
from models.base_model import BaseModel
#from models.domain import Domain

class NginxConfig(BaseModel):
    schema = {
        **BaseModel.schema,
        'domains': {'type': list, 'required': True},
        'certificate_id': {'type': (str, type(None))},
        'host_ip': {'type': str, 'required': True},
        'host_port': {'type': int, 'required': True},
        'host_https': {'type': bool, 'required': True}
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domains = kwargs.get('domains', [])
        self.certificate_id = kwargs.get('certificate_id')
        self.host_ip = kwargs.get('host_ip')
        self.host_port = kwargs.get('host_port')
        self.host_https = kwargs.get('host_https')

    def get_host_url(self) -> str:
        protocol = "https" if self.host_https else "http"
        return f"{protocol}://{self.host_ip}:{self.host_port}"

    def get_domains(self) -> List[object]:
        return self.domains

    def set_domains(self, domains: List[object]):
        self.domains = domains
        self.updated_at = datetime.utcnow()

    def get_certificate_id(self) -> Optional[int]:
        return self.certificate_id

    def set_certificate_id(self, certificate_id: Optional[int]):
        self.certificate_id = certificate_id
        self.updated_at = datetime.utcnow()

    def get_host_ip(self) -> str:
        return self.host_ip

    def set_host_ip(self, host_ip: str):
        self.host_ip = host_ip
        self.updated_at = datetime.utcnow()

    def get_host_port(self) -> int:
        return self.host_port

    def set_host_port(self, host_port: int):
        self.host_port = host_port
        self.updated_at = datetime.utcnow()

    def get_host_https(self) -> bool:
        return self.host_https

    def set_host_https(self, host_https: bool):
        self.host_https = host_https
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        data = super().to_dict()
        data['domains'] = [d.to_dict() if isinstance(d, BaseModel) else d for d in self.domains]
        data['certificate_id'] = self.certificate_id
        data['host_ip'] = self.host_ip
        data['host_port'] = self.host_port
        data['host_https'] = self.host_https
        return data

    @classmethod
    def get_by_host_ip(cls, items, host_ip):
        """
        Specific method to get Nginx configs by host_ip.
        """
        return cls.get_by(items, 'host_ip', host_ip)