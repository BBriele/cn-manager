import os
import logging
from jinja2 import Template
import ssl_manager

CONFIG_DIR = "/etc/nginx/proxy_manager"

logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

TEMPLATES = {
    "http": "templates/proxy_http.conf.j2",
    "https": "templates/proxy_https.conf.j2"
}

def generate_nginx_conf(domain, backend_host, backend_port, use_https=False):
    """Generate a Nginx config file for HTTP or HTTPS"""
    template_path = TEMPLATES["https"] if use_https else TEMPLATES["http"]

    with open(template_path, "r") as f:
        template = Template(f.read())

    conf_content = template.render(domain=domain, backend_host=backend_host, backend_port=backend_port)

    file_path = f"{CONFIG_DIR}/{domain}.conf"
    with open(file_path, "w") as f:
        f.write(conf_content)

    logging.info(f"Nginix config file created: {file_path}")

    if use_https:
        ssl_manager.issue_ssl(domain)  # Emissione automatica del certificato SSL

    return file_path

def reload_nginx():
    """Reload Nginix service"""
    os.system("nginx -s reload")
    logging.info("Nginx successfully reloaded")

def delete_nginx_conf(domain):
    """Delete a Nginx config file"""
    file_path = f"{CONFIG_DIR}/{domain}.conf"
    if os.path.exists(file_path):
        os.remove(file_path)
        reload_nginx()
        ssl_manager.delete_ssl(domain)  # Rimuove certificato SSL se esistente
        logging.info(f"Delete config file: {file_path}")
        return True
    else:
        logging.warning(f"Attempt to delete a non-existent proxy: {domain}")
        return False