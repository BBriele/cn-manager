import os
import logging
from jinja2 import Template
import ssl_manager
import database_manager
from datetime import datetime

CONFIG_DIR = "/etc/nginx/proxy_manager"
os.makedirs(CONFIG_DIR, exist_ok=True)


logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

TEMPLATES = {
    "http": "templates/proxy_http.conf.j2",
    "https": "templates/proxy_https.conf.j2"
}

def generate_nginx_conf(domain, backend_host, backend_port, use_https=False, ssl_certificate=False, eneble_websocket=False):
    """Generate a Nginx config file for HTTP or HTTPS"""
    template_path = TEMPLATES["https"] if ssl_certificate else TEMPLATES["http"]

    id = datetime.timestamp()

    with open(template_path, "r") as f:
        template = Template(f.read())

    domain_list = " ".join(domain)
    print(domain_list)

    if not ssl_certificate:
        conf_content = template.render(id=id, domain=domain_list, backend_host=backend_host, backend_port=backend_port, use_https=use_https, eneble_websocket=eneble_websocket)
    else:
        conf_content = template.render(id=id, domain=domain_list, backend_host=backend_host, backend_port=backend_port, ssl_certificate=ssl_certificate, use_https=use_https, eneble_websocket=eneble_websocket)



    file_path = f"{CONFIG_DIR}/{id}.conf"
    with open(file_path, "w") as f:
        f.write(conf_content)

    logging.info(f"Nginix config file created: {file_path}")

    return id

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

def apply_proxies():
    """Generate Nginx config files for all proxies in the database"""
    proxies = database_manager.get_proxies()
    for proxy in proxies:
        generate_nginx_conf(
            id = proxy["id"],
            domain=proxy["domains"],
            backend_host=proxy["backend_host"],
            backend_port=proxy["backend_port"],
            use_https=proxy.get("use_https", False),
            ssl_certificate=proxy.get("ssl_certificate", False),
            eneble_websocket=proxy.get("enable_websocket", False)
        )
    reload_nginx()
    logging.info("Applied all proxies")