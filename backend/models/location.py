from typing import Optional, Dict, List
from pydantic import BaseModel
import uuid

class Location(BaseModel):
    id: str = uuid.uuid4()  # Generate a unique ID
    name: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "unique_id",
                "name": "My Certificate",
                "path": str,
                "proxy_pass": str,
            }
        }
    }

    def __init__(self, path: str = "/", proxy_pass: str = None):
        super().__init__(path=path, proxy_pass=proxy_pass)