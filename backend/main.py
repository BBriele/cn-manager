from flask import Flask
from routes import general, config, certs, domain
import config as app_config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(app_config.Config)

# Register blueprints
app.register_blueprint(general.bp)
app.register_blueprint(config.bp)
app.register_blueprint(certs.bp)
#app.register_blueprint(proxy.bp)
#app.register_blueprint(dns.bp)
app.register_blueprint(domain.bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)