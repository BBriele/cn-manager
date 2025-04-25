from flask import Blueprint, render_template, request, redirect, url_for
from controllers.nginx_config_controller import NginxConfigController

bp = Blueprint('nginx_config', __name__, url_prefix='/nginx_config')

@bp.route('/')
def list():
    return NginxConfigController.list_view()

@bp.route('/create', methods=['GET', 'POST'])
def create():
    return NginxConfigController.create_view(request)