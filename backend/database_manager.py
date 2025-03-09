import json
import os
from datetime import datetime
import logging

DB_FILE = "data/database.json"

logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure the database file exists
def initialize_database():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"proxies": [], "ssl_certificates": [], "config": {}}, f, indent=4)

def load_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
    logging.info(f"DB saved: {data}")

def add_proxy(proxy_data):
    data = load_data()
    data["proxies"].append(proxy_data)
    save_data(data)

def remove_proxy(proxy_id):
    data = load_data()
    data["proxies"] = [p for p in data["proxies"] if p["id"] != proxy_id]
    save_data(data)

def get_proxies():
    return load_data().get("proxies", [])

def find_proxy_by_id(proxy_id):
    proxies = get_proxies()
    for proxy in proxies:
        if proxy["id"] == proxy_id:
            return proxy
    return None

def add_ssl_certificate(cert_data):
    data = load_data()
    data["ssl_certificates"].append(cert_data)
    save_data(data)

def remove_ssl_certificate(cert_id):
    data = load_data()
    data["ssl_certificates"] = [c for c in data["ssl_certificates"] if c["id"] != cert_id]
    save_data(data)

def get_ssl_certificates():
    return load_data().get("ssl_certificates", [])

def update_config(key, value):
    data = load_data()
    data["config"][key] = value
    save_data(data)

def get_config():
    return load_data().get("config", {})

# Initialize database on first run
initialize_database()
