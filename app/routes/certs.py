from flask import Blueprint, render_template, request, redirect, url_for
from controllers.certificate_controller import CertificateController

bp = Blueprint('certs', __name__, url_prefix='/certs')

@bp.route('/')
def cert_list():
    # TODO: Implement listing certificates
    return render_template('cert_list.html')

@bp.route('/create', methods=['GET', 'POST'])
def create_cert():
    if request.method == 'POST':
        try:
            certificate_data = {
                "email": request.form['email'],
                "name": request.form['cert_name'],
                "domains": [{"name": request.form['domain']}],  # Assuming single domain for now
                "dns_challenge": request.form.get('dns_challenge') == 'on',
                "agree": request.form.get('agree') == 'on'
            }

            CertificateController.create_certificate(certificate_data)

            return redirect(url_for('certs.cert_list'))
        except Exception as e:
            return render_template('cert_create.html', errors=[str(e)])

    return render_template('cert_create.html', errors=None)