import os
import importlib.util
import uuid
from datetime import datetime
import json
import subprocess  # Per eseguire Certbot o ACME client

import config as app_config
from models.base_model import BaseModel
from models.dns_provider import DNSProvider


class DNSConfig(BaseModel):
    model_name = "dns_configs"
    schema = {
        **BaseModel.schema,
        'provider_type': {'type': str, 'required': True},
        'config_data': {'type': dict, 'required': True}
    }

    PROVIDERS = {}

    @classmethod
    def load_plugins(cls, plugins_directory="plugins/custom_dns"):
        """
        Scans the plugins directory and dynamically loads all available DNS providers.
        """
        if not os.path.exists(plugins_directory):
            os.makedirs(plugins_directory)  # Create the directory if it doesn't exist

        for filename in os.listdir(plugins_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                module_path = os.path.join(plugins_directory, filename)

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, DNSProvider) and attribute is not DNSProvider:
                        cls.PROVIDERS[module_name.lower()] = attribute

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

    def create_record(self, domain, record_type, value):
        return self.provider.create_record(domain, record_type, value)

    def delete_record(self, domain, record_type, value):
        return self.provider.delete_record(domain, record_type, value)

    def get_records(self, domain):
        return self.provider.get_records(domain)

    def update_record(self, domain, record_type, old_value, new_value):
        return self.provider.update_record(domain, record_type, old_value, new_value)
    
    def request_ssl_certificate(self, domain):
        """
        Requests an SSL certificate using DNS-01 challenge and saves it in the configured path.
        """
        challenge_value = "_acme-challenge.example.com"  # Questo valore sarà ricevuto dall'ACME client

        # Percorso della cartella certificati definito in config.py
        cert_path = app_config.PATH_TO_PROJ_CERT
        if not os.path.exists(cert_path):
            os.makedirs(cert_path)  # Creiamo la cartella se non esiste

        print(f"Requesting SSL certificate for {domain} using {self.provider_type}...")
        self.provider.perform_dns_challenge(domain, challenge_value)

        # Percorso in cui verrà salvato il certificato
        full_cert_path = os.path.join(cert_path, domain)

        # Eseguiamo Certbot o un altro client ACME per ottenere il certificato
        command = [
            "certbot",
            "certonly",
            "--manual",
            "--preferred-challenges",
            "dns",
            "--manual-auth-hook",
            f"echo 'Challenge for {domain} completed'",
            "--manual-cleanup-hook",
            f"echo 'Cleanup for {domain} completed'",
            "--agree-tos",
            "--config-dir", full_cert_path,  # Salviamo i certificati nella cartella configurata
            "-d", domain
        ]

        try:
            subprocess.run(command, check=True)
            print(f"SSL Certificate for {domain} obtained successfully! Saved in {full_cert_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error requesting SSL certificate: {e}")

    def to_dict(self):
        data = super().to_dict()
        data['provider_type'] = self.provider_type
        data['config_data'] = self.config_data
        return data
