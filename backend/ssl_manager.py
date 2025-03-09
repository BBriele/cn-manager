import os
import logging
import uuid
from datetime import datetime, timedelta
import database_manager

CERT_DIR = "/etc/letsencrypt/live/"

logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def is_certbot_installed():
    return os.system("which certbot > /dev/null") == 0

if not is_certbot_installed():
    logging.critical("Certbot non è installato! Installalo prima di procedere.")

def issue_ssl(cert_type, credentials, domain_list=[]):
    """Genera un certificato SSL per il dominio usando Certbot o Cloudflare"""
    logging.info(f"Richiesta certificato SSL di tipo {cert_type}")

    creating_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id = hash(creating_at)
    
    domains = " ".join([f"-d {domain}" for domain in domain_list])
    logging.info(f"Domain list for certificate {domains}")
    
    if cert_type == "letsencrypt":
        command = f"certbot certonly --nginx \
                    --config-dir {CERT_DIR+str(id)} \
                    --non-interactive \
                    --agree-tos \
                    -m {credentials['email']} \
                    {domains} "
    elif cert_type == "cloudflare":
        command = f"certbot certonly \
                    --config-dir {CERT_DIR+str(id)} \
                    --dns-cloudflare \
                    --dns-cloudflare-credentials /root/cn-manager/backend/.secrect/certbot/cloudflare.ini \
                    --dns-cloudflare-propagation-seconds 20\
                    --non-interactive \
                    --agree-tos \
                    --post-hook 'nginx -s reload' \
                    -m {credentials['email']} \
                    {domains}"
        
    else:
        logging.error(f"Tipo di certificato non supportato: {cert_type}")
        return False
    
    result = os.system(command)
    
    if result == 0:
        logging.info(f"Certificato SSL generato con successo")
        expires_at = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
        cert_info = {
            "id": id,
            "type": cert_type,
            "domain_list": domain_list,
            "created_at": creating_at,
            "expires_at": expires_at,
            "status": "active",
            "path": f"{CERT_DIR}{id}"
        }
        logging.info(f"Succesfully generated {cert_type} certificate")
        return cert_info
    else:
        logging.error(f"Errore nella generazione del certificato SSL per {result}")
        return False

def delete_ssl(cert_name):
    """Rimuove il certificato SSL di un dominio"""
    logging.info(f"Rimozione certificato SSL per {cert_name}")

    cert_path = f"/etc/letsencrypt/live/{cert_name}"
    if os.path.exists(cert_path):
        os.system(f"certbot delete --cert-name {cert_name}")
        logging.info(f"Certificato SSL rimosso per {cert_name}")
        return True
    else:
        logging.warning(f"Nessun certificato SSL trovato per {cert_name}")
        return False