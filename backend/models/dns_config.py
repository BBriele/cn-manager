import uuid
from datetime import datetime
from models.base_model import BaseModel
import json

class DNSConfig(BaseModel):
    schema = {
        **BaseModel.schema,
        'provider_type': {'type': str, 'required': True},
        'config_data': {'type': dict, 'required': True}
    }

    def __init__(self, **kwargs):
        self.provider_type = kwargs.get('provider_type') #Removed
        self.config_data = kwargs.get('config_data') #Removed
        super().__init__(**kwargs)

    def get_provider_type(self) -> str:
        return self.provider_type

    def set_provider_type(self, provider_type: str):
        self.provider_type = provider_type
        self.updated_at = datetime.utcnow()

    def get_config_data(self) -> dict:
        return self.config_data

    def set_config_data(self, config_data: dict):
        self.config_data = config_data
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        data = super().to_dict()
        data['provider_type'] = self.provider_type
        data['config_data'] = self.config_data
        return data