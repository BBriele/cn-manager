from flask import Blueprint, render_template, request, redirect, url_for
import logging

from models.dns_config import DNSConfig
from plugins.custom_dns.dns_provider import DNSProvider

from utility import db, logger  # Usa il database manager globale



class DNSConfigController:
    @staticmethod
    def list_dns_configs():
        return DNSConfig.list()

    @staticmethod
    def get_dns_config(dns_config_id):
        return DNSConfig.get_all()

    @staticmethod
    def create_dns_config(dns_config_data):
        dns_config = DNSConfig(**dns_config_data)
        db.create(DNSConfig.model_name, dns_config)
        return dns_config

    @staticmethod
    def update_dns_config(dns_config_id, dns_config_data):
        dns_config = DNSConfig.get(dns_config_id)
        if not dns_config:
            raise ValueError("DNS Config not found")
        for key, value in dns_config_data.items():
            setattr(dns_config, key, value)
        db.update(DNSConfig.model_name, dns_config_id, dns_config)
        return dns_config

    @staticmethod
    def delete_dns_config(dns_config_id):
        dns_config = DNSConfig.get(dns_config_id)
        if not dns_config:
            raise ValueError("DNS Config not found")
        db.delete(DNSConfig.model_name, dns_config_id)
        return True
    
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

#region Views Functions

    def view_list(self):
        """
        Render a list view.
        """
        dns_configs = self.list_dns_configs()
        return render_template('dns_config/list.html', dns_configs=dns_configs)
    
    def view_create(self):
        """
        Render a create view.
        """
        dns_providers = DNSProvider.get_records
        return render_template('dns_config/create.html', dns_providers=dns_providers)
    
#endregion