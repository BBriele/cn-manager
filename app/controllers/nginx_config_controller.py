from flask import Blueprint, render_template, request, redirect, url_for
import logging

from models.nginx_config import NginxConfig
from services.nginx_manager import NginxManager
from utility import db, logger  # Usa il database manager globale


class NginxConfigController:
    def __init__(self):
        self.nginx_manager = NginxManager()

    def create_nginx_config(self, config_data: dict) -> NginxConfig:
        """
        Creates a new Nginx configuration and saves it to the database.
        """
        try:
            nginx_config = NginxConfig(**config_data)
            db.create("nginx_configs", nginx_config)
            self.nginx_manager.create_config(nginx_config)
            return nginx_config
        except Exception as e:
            raise e

    def get_nginx_config(self, config_id: str) -> NginxConfig:
        """
        Retrieves an Nginx configuration from the database.
        """
        nginx_config = db.get("nginx_configs", config_id)
        if not nginx_config:
            raise ValueError(f"NginxConfig with id {config_id} not found")
        return nginx_config

    def update_nginx_config(self, config_id: str, config_data: dict) -> NginxConfig:
        """
        Updates an existing Nginx configuration in the database.
        """
        try:
            nginx_config = NginxConfig(**config_data)
            db.update("nginx_configs", config_id, nginx_config)
            self.nginx_manager.create_config(nginx_config)  # Reapply the config to Nginx
            return nginx_config
        except Exception as e:
            raise e

    def delete_nginx_config(self, config_id: str):
        """
        Deletes an Nginx configuration from the database.
        """
        nginx_config = self.get_nginx_config(config_id)
        self.nginx_manager.delete_config(nginx_config.domains[0].name)  # Delete the Nginx config file
        db.delete("nginx_configs", config_id)

    def list_nginx_configs(self) -> list[NginxConfig]:
        """
        Lists all Nginx configurations from the database.
        """
        return db.list("nginx_configs")

#region View Functions

    def list_view():
        #logging: Rendering nginx_config list view
        logger.info("Rendering nginx_config list view")
        """
        Renders the nginx_config list view.
        """
        domains = db.list("nginx_config")
        return render_template('components/nginx_config/list.html', domains=domains)
    
    @classmethod
    def create_view(cls, request):
        #logging: Rendering create nginx_config view
        logger.info("Rendering create nginx_config view")
        """
        Renders the create nginx_config view.
        """
        if request.method == 'POST':
            try:
                data = request.form

                cls.create_nginx_config(data)
                return redirect(url_for('nginx_config.list'))
            except Exception as e:
                return render_template('components/nginx_config/create.html', errors=[str(e)])

        return render_template('components/nginx_config/create.html', errors=None)


#endregion