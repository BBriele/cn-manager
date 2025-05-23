from flask import Blueprint, render_template, request, redirect, url_for
from controllers.domain_controller import DomainController

bp = Blueprint('domain', __name__, url_prefix='/domain')

@bp.route('/')
def list():
    return DomainController.list_view()

@bp.route('/create', methods=['GET', 'POST'])
def create():
    return DomainController.create_view(request)