from flask import Blueprint, render_template, request, redirect, url_for
from controllers.certificate_controller import CertificateController

bp = Blueprint('certificate', __name__, url_prefix='/certificate')

@bp.route('/')
def list():
    return CertificateController.list_view()

@bp.route('/create', methods=['GET', 'POST'])
def create():
    return CertificateController.create_view(request)

@bp.route('/edit', methods=['GET', 'POST'])
def edit():
    return CertificateController.edit_view(request)

@bp.route('/delete', methods=['GET', 'POST'])
def delete():
    return CertificateController.delete_view(request)
