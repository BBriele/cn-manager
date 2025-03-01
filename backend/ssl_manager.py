import os
import logging

logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def issue_ssl(domain):
    """Genera un certificato SSL per il dominio usando Certbot"""
    logging.info(f"Richiesta certificato SSL per {domain}")
    
    command = f"certbot certonly --nginx --non-interactive --agree-tos -m admin@{domain} -d {domain}"
    result = os.system(command)
    
    if result == 0:
        logging.info(f"Certificato SSL generato con successo per {domain}")
    else:
        logging.error(f"Errore nella generazione del certificato SSL per {domain}")

def delete_ssl(domain):
    """Rimuove il certificato SSL di un dominio"""
    logging.info(f"Rimozione certificato SSL per {domain}")

    cert_path = f"/etc/letsencrypt/live/{domain}"
    if os.path.exists(cert_path):
        os.system(f"certbot delete --cert-name {domain}")
        logging.info(f"Certificato SSL rimosso per {domain}")
    else:
        logging.warning(f"Nessun certificato SSL trovato per {domain}")
