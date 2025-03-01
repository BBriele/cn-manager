from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
import nginx_manager
import logging

HOST = "0.0.0.0"
PORT = 8080

# Configurazione logging
logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class ProxyManagerServer(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        """Set the response header"""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _handle_exception(self, error_message, status_code=500):
        """Manage errors and return a JSON"""
        logging.error(f"Error: {error_message}")
        self._set_headers(status_code)
        self.wfile.write(json.dumps({"error": error_message}).encode("utf-8"))

    def do_POST(self):
        """Create a new proxy (HTTP o HTTPS)"""
        if self.path == "/add_proxy":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                params = json.loads(post_data.decode("utf-8"))

                domain = params.get("domain")
                backend_host = params.get("backend_host")
                backend_port = params.get("backend_port")
                use_https = params.get("use_https", False)

                if not domain or not backend_host or not backend_port:
                    self._handle_exception("Missing Parameters", 400)
                    return

                nginx_manager.generate_nginx_conf(domain, backend_host, backend_port, use_https)
                nginx_manager.reload_nginx()

                logging.info(f"Proxy created: {domain} (HTTPS: {use_https})")

                self._set_headers(201)
                self.wfile.write(json.dumps({"message": "Proxy created"}).encode("utf-8"))

            except json.JSONDecodeError:
                self._handle_exception("JSON not valid", 400)
            except Exception as e:
                self._handle_exception(str(e), 500)

    def do_DELETE(self):
        """manage proxy deletion"""
        if self.path.startswith("/delete_proxy?"):
            try:
                query = self.path.split("?")[1]
                params = parse_qs(query)
                domain = params.get("domain", [None])[0]

                if not domain:
                    self._handle_exception("Specify the domain", 400)
                    return

                if nginx_manager.delete_nginx_conf(domain):
                    logging.info(f"Proxy deleted: {domain}")
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Proxy deleted"}).encode("utf-8"))
                else:
                    self._handle_exception("Proxy not found", 404)

            except Exception as e:
                self._handle_exception(str(e), 500)

def run_server():
    """Start the server"""
    try:
        server_address = (HOST, PORT)
        httpd = HTTPServer(server_address, ProxyManagerServer)
        logging.info(f"Server started on {HOST}:{PORT}")
        httpd.serve_forever()
    except Exception as e:
        logging.critical(f"Critic error: {str(e)}")

if __name__ == "__main__":
    run_server()
