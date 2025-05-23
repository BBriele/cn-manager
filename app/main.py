from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os

from routes import general, config, domain, dns_config, nginx_config, certificate
import config as app_config
from utility import db, logger


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config.Config)

    # Register blueprints
    app.register_blueprint(general.bp)
    app.register_blueprint(config.bp)
    app.register_blueprint(certificate.bp)
    app.register_blueprint(dns_config.bp)
    app.register_blueprint(nginx_config.bp)
    app.register_blueprint(domain.bp)

    return app

if __name__ == "__main__":
    logger.info("Starting the application...")
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)