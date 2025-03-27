from flask import Flask
from routes import general, config, certs, domain
import config as app_config
import logging
import os

# Configure logging
log_file = 'cn_manager.log'
log_level = logging.INFO
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)

# Create a formatter
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

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
    logger.info("Starting the application...")
    app.run(host='0.0.0.0', port=8000, debug=True)