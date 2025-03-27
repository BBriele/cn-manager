import uuid
from datetime import datetime
from models.base_model import BaseModel

class ProxyRule(BaseModel):
    model_name = "proxy_rules"  # Define the model name
    schema = {
        **BaseModel.schema,
        'nginx_config_id': {'type': str, 'required': True}
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nginx_config_id = kwargs.get('nginx_config_id')

    def get_nginx_config_id(self) -> str:
        return self.nginx_config_id

    def set_nginx_config_id(self, nginx_config_id: str):
        self.nginx_config_id = nginx_config_id
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        data = super().to_dict()
        data['nginx_config_id'] = self.nginx_config_id
        return data

    @classmethod
    def get_by_nginx_config_id(cls, items, nginx_config_id):
        """
        Specific method to get proxy rules by nginx_config_id.
        """
        return cls.get_by(items, 'nginx_config_id', nginx_config_id)