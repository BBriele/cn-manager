import os
import importlib.util
import uuid
from datetime import datetime
import json
import subprocess  # Per eseguire Certbot o ACME client

import config as app_config
from models.base_model import BaseModel
from plugins.custom_dns.dns_provider import DNSProvider


class DNSConfig(BaseModel):
    model_name = "dns_configs"
    schema = {
        **BaseModel.schema,
        'provider_type': {'type': str, 'required': True},
        'config_data': {'type': dict, 'required': True}
    }

    PROVIDERS = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = self.get_provider()

    def get_provider(self):
        """
        Factory method to get the correct DNS provider class.
        """
        provider_class = self.PROVIDERS.get(self.provider_type.lower())
        if not provider_class:
            raise ValueError(f"Unsupported DNS provider: {self.provider_type}")
        return provider_class(self.config_data)