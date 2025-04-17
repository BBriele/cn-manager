import nginx
import os
from models.nginx_config import NginxConfig
from models.domain import Domain
from db_manager import db  # Usa il database manager globale

class NginxManager:
    def __init__(self, config_dir='/etc/nginx/conf.d'):
        self.config_dir = config_dir

    def create_config(self, nginx_config: NginxConfig):
        '''
        nginx_config: NginxConfig object
        '''
        config_name = nginx_config.domains[0].name  # Use the first domain name as the config name

        # Create a new server block
        server = nginx.Server()
        server.add_directive('listen', '80')
        server.add_directive('server_name', ' '.join([domain.name for domain in nginx_config.domains]))

        location = nginx.Location('/')
        location.add_directive('proxy_pass', f"http{ 's' if nginx_config.host_https else '' }://{nginx_config.host_ip}:{nginx_config.host_port}")
        server.add_location(location)

        if nginx_config.certificate_id:
            certificate = db.get("certificates", nginx_config.certificate_id)
            if certificate:
                server.add_directive('listen', '443 ssl')
                server.add_directive('ssl_certificate', certificate.certificate_path)
                server.add_directive('ssl_certificate_key', certificate.private_key_path)

        cfg = nginx.Conf()
        cfg.add_server(server)
        try:
            nginx.dumpf(cfg, f'{self.config_dir}/{config_name}.conf')
            self.reload_nginx()
        except Exception as e:
            print(f"Error saving Nginx configuration: {e}")

    def save_config(self, config: nginx.Conf, filename: str):
        try:
            nginx.dumpf(config, filename)
            self.reload_nginx()
        except Exception as e:
            print(f"Error saving Nginx configuration: {e}")

    def reload_nginx(self):
        # Reload Nginx (requires sudo)
        os.system('sudo nginx -s reload')

    def delete_config(self, config_name: str):
        try:
            os.remove(f'{self.config_dir}/{config_name}.conf')
            self.reload_nginx()
        except FileNotFoundError:
            print(f"Config file {config_name}.conf not found.")
        except Exception as e:
            print(f"Error deleting Nginx configuration: {e}")