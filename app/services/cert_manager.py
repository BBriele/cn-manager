import subprocess
import os

from models.domain import Domain
from models.certificate import Certificate

class CertManager:
    def __init__(self, cert_dir='/etc/nginx/certs'):
        self.cert_dir = cert_dir
        os.makedirs(cert_dir, exist_ok=True)

    def generate_certificate(self, certificate: Certificate):
        """
        Generates a certificate using Certbot.
        """
        domain_names = [domain.name for domain in certificate.domains]
        email = certificate.email
        cert_name = certificate.name.replace(" ", "_")  # Sanitize certificate name

        certificate_path = os.path.join(self.cert_dir, f"{cert_name}.pem")
        private_key_path = os.path.join(self.cert_dir, f"{cert_name}.key")

        # Construct the Certbot command
        command = [
            "certbot", "certonly",
            "--standalone",  # Use the standalone authenticator
            "-d", ",".join(domain_names),  # Specify the domain names
            "--email", email,  # Specify the email address
            "--agree-tos",  # Agree to the Let's Encrypt terms of service
            "--non-interactive",  # Run in non-interactive mode
            "--cert-name", cert_name, # Specify the certificate name
            "--cert-path", certificate_path,
            "--key-path", private_key_path
        ]

        if certificate.dns_challenge:
            # Add DNS challenge options
            command.extend([
                "--manual",
                "--preferred-challenges", "dns",
                "--manual-auth-hook", f"echo 'auth hook'",  # Replace with your actual auth hook
                "--manual-cleanup-hook", f"echo 'cleanup hook'"  # Replace with your actual cleanup hook
            ])

        try:
            # Execute the Certbot command
            subprocess.run(command, check=True)

            # Update the certificate object with the generated paths
            certificate.certificate_path = certificate_path
            certificate.private_key_path = private_key_path

        except subprocess.CalledProcessError as e:
            print(f"Certbot failed with error: {e}")
            raise

        return certificate