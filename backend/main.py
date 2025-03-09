from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
import logging
from dotenv import load_dotenv
from datetime import datetime

import nginx_manager
import database_manager
import ssl_manager
import config_manager

HOST = "0.0.0.0"
PORT = 8080

logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")





class ProxyManagerServer(BaseHTTPRequestHandler):
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _handle_exception(self, error_message, status_code=500):
        logging.error(f"Error: {error_message}")
        self._set_headers(status_code)
        self.wfile.write(json.dumps({"error": error_message}).encode("utf-8"))
    
    def do_GET(self):
        if self.path == "/proxies":
            proxies = database_manager.get_proxies()
            self._set_headers(200)
            self.wfile.write(json.dumps(proxies).encode("utf-8"))
        
        elif self.path == "/certificates":
            certificates = database_manager.get_ssl_certificates()
            self._set_headers(200)
            self.wfile.write(json.dumps(certificates).encode("utf-8"))
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/proxies":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                params = json.loads(post_data.decode("utf-8"))

                domain_list = params.get("domains", [])
                backend_host = params.get("backend_host")
                backend_port = params.get("backend_port")
                use_https = params.get("use_https", False)
                ssl_certificate = params.get("ssl_certificate", None)
                enable_websocket = params.get("enable_websocket", False)

                if not domain_list or not backend_host or not backend_port:
                    self._handle_exception("Missing parameters", 400)
                    return

                new_proxy = nginx_manager.generate_nginx_conf(domain_list, backend_host, backend_port, use_https, ssl_certificate, enable_websocket)
                nginx_manager.reload_nginx()

                params["id"] = new_proxy
                database_manager.add_proxy(params)
                
                logging.info(f"Proxy created: {domain_list}")

                self._set_headers(201)
                self.wfile.write(json.dumps({"message": "Proxy created"}).encode("utf-8"))
            
            except json.JSONDecodeError:
                self._handle_exception("Invalid JSON", 400)
            except Exception as e:
                self._handle_exception(str(e), 500)

        elif self.path == "/certificates":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                params = json.loads(post_data.decode("utf-8"))

                cert_type = params.get("type")  # "letsencrypt" or "cloudflare"
                credentials = params.get("credentials")
                domain_list = params.get("domains", [])

                if not cert_type or not credentials:
                    self._handle_exception("Missing parameters", 400)
                    return

                new_cert = ssl_manager.issue_ssl(cert_type, credentials, domain_list)
                if new_cert: database_manager.add_ssl_certificate(new_cert)

                self._set_headers(201)
                self.wfile.write(json.dumps({"message": "Certificate added"}).encode("utf-8"))
            
            except json.JSONDecodeError:
                self._handle_exception("Invalid JSON", 400)
            except Exception as e:
                self._handle_exception(str(e), 500)
    
    def do_DELETE(self):
        if self.path.startswith("/proxies?"):
            try:
                query = self.path.split("?")[1]
                params = parse_qs(query)
                domain = params.get("domain", [None])[0]

                if not domain:
                    self._handle_exception("Specify the domain", 400)
                    return

                if database_manager.delete_proxy(domain):
                    nginx_manager.apply_proxies()
                    logging.info(f"Proxy deleted: {domain}")
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Proxy deleted"}).encode("utf-8"))
                else:
                    self._handle_exception("Proxy not found", 404)

            except Exception as e:
                self._handle_exception(str(e), 500)
    
        elif self.path.startswith("/certificates?"):
            try:
                query = self.path.split("?")[1]
                params = parse_qs(query)
                cert_name = params.get("name", [None])[0]

                if not cert_name:
                    self._handle_exception("Specify the certificate name", 400)
                    return

                if database_manager.delete_certificate(cert_name):
                    logging.info(f"Certificate deleted: {cert_name}")
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Certificate deleted"}).encode("utf-8"))
                else:
                    self._handle_exception("Certificate not found", 404)
            
            except Exception as e:
                self._handle_exception(str(e), 500)

def run_server():
    try:
        server_address = (HOST, PORT)
        httpd = HTTPServer(server_address, ProxyManagerServer)
        logging.info(f"Server started on {HOST}:{PORT}")
        httpd.serve_forever()
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    run_server()
