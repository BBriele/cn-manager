from flask import Blueprint, render_template, request, redirect, url_for
from controllers.dns_config_controller import DNSConfigController

bp = Blueprint('dns_config', __name__, url_prefix='/dns_config')

@bp.route('/')
def dns_config_list():
    dns_configs = DNSConfigController.list_dns_configs()
    return render_template('components/dns_config/list.html', dns_configs=dns_configs)

@bp.route('/create', methods=['GET', 'POST'])
def create_dns_config():
    if request.method == 'POST':
        try:
            dns_config_data = {
                "provider_type": request.form['provider_type'],
                "config_data": request.form['config_data']  # Assuming this is a JSON string
            }
            DNSConfigController.create_dns_config(dns_config_data)
            return redirect(url_for('dns_config.dns_config_list'))
        except Exception as e:
            return render_template('components/dns_config/create.html', errors=[str(e)])

    return render_template('components/dns_config/create.html', errors=None)

@bp.route('/<dns_config_id>/update', methods=['GET', 'POST'])
def update_dns_config(dns_config_id):
    dns_config = DNSConfigController.get_dns_config(dns_config_id)

    if request.method == 'POST':
        try:
            dns_config_data = {
                "provider_type": request.form['provider_type'],
                "config_data": request.form['config_data']  # Assuming this is a JSON string
            }
            DNSConfigController.update_dns_config(dns_config_id, dns_config_data)
            return redirect(url_for('dns_config.dns_config_list'))
        except Exception as e:
            return render_template('components/dns_config/update.html', dns_config=dns_config, errors=[str(e)])

    return render_template('components/dns_config/update.html', dns_config=dns_config, errors=None)

@bp.route('/<dns_config_id>/delete', methods=['POST'])
def delete_dns_config(dns_config_id):
    try:
        DNSConfigController.delete_dns_config(dns_config_id)
        return redirect(url_for('components/dns_config.dns_config_list'))
    except Exception as e:
        return f"Error deleting DNS config: {str(e)}"