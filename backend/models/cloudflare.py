import uuid
from datetime import datetime
from models.base_model import BaseModel

class CloudflareConfig(BaseModel):
    schema = {
        **BaseModel.schema,
        'api_token': {'type': str, 'required': True},
        'zone_id': {'type': str, 'required': True}
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_token = kwargs.get('api_token')
        self.zone_id = kwargs.get('zone_id')

    def get_api_token(self) -> str:
        return self.api_token

    def get_zone_id(self) -> str:
        return self.zone_id

    def set_api_token(self, api_token: str):
        self.api_token = api_token
        self.updated_at = datetime.utcnow()

    def set_zone_id(self, zone_id: str):
        self.zone_id = zone_id
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        data = super().to_dict()
        data['api_token'] = self.api_token
        data['zone_id'] = self.zone_id
        return data

    @classmethod
    def get_by_zone_id(cls, items, zone_id):
        """
        Specific method to get Cloudflare configs by zone_id.
        """
        return cls.get_by(items, 'zone_id', zone_id)
