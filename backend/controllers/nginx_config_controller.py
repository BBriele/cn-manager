from models.nginx_config import NginxConfig
from services.database_manager import DatabaseManager
from services.nginx_manager import NginxManager

db_manager = DatabaseManager()
nginx_manager = NginxManager()

def create_nginx_config(config_data: dict) -> NginxConfig:
    """
    Creates a new Nginx configuration and saves it to the database.
    """
    try:
        nginx_config = NginxConfig(**config_data)
        db_manager.create("nginx_configs", nginx_config)
        nginx_manager.create_config(nginx_config)
        return nginx_config
    except Exception as e:
        raise e

def get_nginx_config(config_id: str) -> NginxConfig:
    """
    Retrieves an Nginx configuration from the database.
    """
    nginx_config = db_manager.get("nginx_configs", config_id)
    if not nginx_config:
        raise ValueError(f"NginxConfig with id {config_id} not found")
    return nginx_config

def update_nginx_config(config_id: str, config_data: dict) -> NginxConfig:
    """
    Updates an existing Nginx configuration in the database.
    """
    try:
        nginx_config = NginxConfig(**config_data)
        db_manager.update("nginx_configs", config_id, nginx_config)
        nginx_manager.create_config(nginx_config)  # Reapply the config to Nginx
        return nginx_config
    except Exception as e:
        raise e

def delete_nginx_config(config_id: str):
    """
    Deletes an Nginx configuration from the database.
    """
    nginx_config = get_nginx_config(config_id)
    nginx_manager.delete_config(nginx_config.domains[0].name)  # Delete the Nginx config file
    db_manager.delete("nginx_configs", config_id)

def list_nginx_configs() -> list[NginxConfig]:
    """
    Lists all Nginx configurations from the database.
    """
    return db_manager.list("nginx_configs")