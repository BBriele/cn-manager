from pydantic import BaseModel, field_validator
import uuid
import time

class Domain(BaseModel):
    id: str = str(uuid.uuid4())  # Generate a unique ID
    name: str

    @field_validator('name')
    def name_must_be_a_valid_domain(cls, v):
        # Add more robust domain validation if needed
        if "." not in v:
            raise ValueError('Not a valid domain')
        return v

    def __str__(self):
        return self.name

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "unique_id",
                "name": "example.com"
            }
        }
    }