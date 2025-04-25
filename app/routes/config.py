from flask import Blueprint, render_template, request, redirect, url_for
from services.nginx_manager import NginxManager
from models.nginx_config import NginxConfig

bp = Blueprint('config', __name__, url_prefix='/config')

nginx_manager = NginxManager()

@bp.route('/')
def list():
    # This is just a placeholder, you'll need to read the actual configs
    configs = [NginxConfig("example.com", "http://localhost:8080")]
    return render_template('config_list.html', configs=configs)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        server_name = request.form['server_name']
        proxy_pass = request.form['proxy_pass']
        ssl_certificate = request.form.get('ssl_certificate')
        ssl_certificate_key = request.form.get('ssl_certificate_key')

        nginx_config = NginxConfig(server_name, proxy_pass, ssl_certificate, ssl_certificate_key)
        nginx_manager.create_config("new_config", nginx_config) # You might want to generate a unique name

        return redirect(url_for('config.config_list'))
    return render_template('config_create.html')