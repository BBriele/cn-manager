from pydantic import BaseModel, SecretStr
import uuid
import time

class CloudflareConfig(BaseModel):
    id: str = str(uuid.uuid4())  # Generate a unique ID
    api_token: SecretStr
    zone_id: str

    def get_api_token(self) -> str:
        return self.api_token.get_secret_value()

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "unique_id",
                "api_token": "your_cloudflare_api_token",
                "zone_id": "your_cloudflare_zone_id"
            }
        }
    }