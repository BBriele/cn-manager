from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import uuid
import time

from models.domain import Domain

class NginxConfig(BaseModel):
    id: str = str(uuid.uuid4())  # Generate a unique ID
    domains: List[Domain]
    certificate_id: Optional[int] = None
    host_ip: str
    host_port: int
    host_https: bool

    def get_host_url(self) -> str:
        protocol = "https" if self.host_https else "http"
        return f"{protocol}://{self.host_ip}:{self.host_port}"

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "unique_id",
                "domains": [{"id": "unique_id", "name": "example.com"}],
                "certificate_id": "unique_id",
                "host_ip": "127.0.0.1",
                "host_port": 8000,
                "host_https": False
            }
        }
    }