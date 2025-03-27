from models.dns_config import DNSConfig

class DNSConfigController:
    @staticmethod
    def list_dns_configs():
        return DNSConfig.query.all()

    @staticmethod
    def get_dns_config(dns_config_id):
        return DNSConfig.get_all()

    @staticmethod
    def create_dns_config(dns_config_data):
        dns_config = DNSConfig(**dns_config_data)
        dns_config.save()
        return dns_config

    @staticmethod
    def update_dns_config(dns_config_id, dns_config_data):
        dns_config = DNSConfig.query.get(dns_config_id)
        if not dns_config:
            raise ValueError("DNS Config not found")
        for key, value in dns_config_data.items():
            setattr(dns_config, key, value)
        dns_config.save()
        return dns_config

    @staticmethod
    def delete_dns_config(dns_config_id):
        dns_config = DNSConfig.query.get(dns_config_id)
        if not dns_config:
            raise ValueError("DNS Config not found")
        dns_config.delete()