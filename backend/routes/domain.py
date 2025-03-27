from flask import Blueprint, render_template, request, redirect, url_for
from controllers.domain_controller import DomainController

bp = Blueprint('domain', __name__, url_prefix='/domain')

@bp.route('/')
def domain_list():
    domains = DomainController.list_domains()
    return render_template('domain_list.html', domains=domains)

@bp.route('/create', methods=['GET', 'POST'])
def create_domain():
    if request.method == 'POST':
        try:
            domain_data = {
                "name": request.form['name']
            }
            DomainController.create_domain(domain_data)
            return redirect(url_for('domain.domain_list'))
        except Exception as e:
            return render_template('domain_create.html', errors=[str(e)])

    return render_template('domain_create.html', errors=None)