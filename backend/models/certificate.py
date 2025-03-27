from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
import uuid
import time


from models.domain import Domain
from models.cloudflare import CloudflareConfig

class Certificate(BaseModel):
    id: str = str(uuid.uuid4())  # Generate a unique ID
    email: EmailStr
    name: str
    domains: List[Domain]
    dns_challenge: bool
    cloudflare_config: Optional[CloudflareConfig] = None
    agree: bool
    certificate_path: Optional[str] = None
    private_key_path: Optional[str] = None

    @field_validator('cloudflare_config')
    def cloudflare_config_must_be_present_if_dns_challenge_is_true(cls, v, values):
        if values.get('dns_challenge') and v is None:
            raise ValueError('Cloudflare config must be provided when DNS challenge is enabled')
        return v
    
    def get_domain_names(self) -> List[str]:
        return [domain.name for domain in self.domains]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "unique_id",
                "email": "test@example.com",
                "name": "My Certificate",
                "domains": [{"id": str(uuid.uuid4()), "name": "example.com"}],
                "dns_challenge": True,
                "cloudflare_config": {"api_token": "your_cloudflare_api_token", "zone_id": "your_cloudflare_zone_id"},
                "agree": True,
                "certificate_path": "/path/to/certificate.pem",
                "private_key_path": "/path/to/private_key.pem"
            }
        }
    }