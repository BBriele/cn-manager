from models.dns_provider import DNSProvider

class CloudflareDNS(DNSProvider):
    def create_record(self, domain, record_type, value):
        return f"Cloudflare: Creating {record_type} record for {domain} with value {value}"

    def delete_record(self, domain, record_type, value):
        return f"Cloudflare: Deleting {record_type} record for {domain} with value {value}"

    def get_records(self, domain):
        return f"Cloudflare: Fetching DNS records for {domain}"

    def update_record(self, domain, record_type, old_value, new_value):
        return f"Cloudflare: Updating {record_type} record for {domain} from {old_value} to {new_value}"
