from pydantic import BaseModel
import uuid
import time

class ProxyRule(BaseModel):
    id: int = str(uuid.uuid4())  # Generate a unique ID
    nginx_config_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "unique_id",
                "nginx_config_id": "unique_id"
            }
        }
    }