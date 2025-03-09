from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum

class SSLProviderType(Enum):
    """SSL certificate provider types"""
    LETS_ENCRYPT = "letsencrypt"
    CLOUDFLARE = "cloudflare"

class ChallengeType(Enum):
    HTTP = "http"
    DNS = "dns"

class CertificateStatus(Enum):
    PENDING = "pending"
    VALID = "valid"
    EXPIRED = "expired"
    REVOKED = "revoked"
    FAILED = "failed"

@dataclass
class ProxyConfig:
    """Proxy host configuration model"""
    id: Optional[str] = None
    domains: List[str] = None
    backend_host: str = None
    backend_port: int = None
    use_https: bool = False
    ssl_certificate_id: Optional[str] = None
    enable_websocket: bool = False
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class SSLCertificate(BaseModel):
    """SSL Certificate model with challenge tracking"""
    id: str
    name: str
    provider: SSLProviderType
    domains: List[str]
    wildcard: bool
    challenge_type: ChallengeType
    status: CertificateStatus
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    last_renewal: Optional[datetime]
    cloudflare_zone_id: Optional[str]
    cloudflare_record_ids: Optional[List[str]]



class LetsEncryptManager(SSLManager):
    """Let's Encrypt certificate manager with multiple challenge support"""
    
    def __init__(self, cert_path: str = "/etc/nginx/certs", 
                 config_path: str = "/etc/letsencrypt"):
        self.cert_path = cert_path
        self.config_path = config_path
        self._ensure_paths()
    
    def _ensure_paths(self):
        """Ensure required directories exist"""
        os.makedirs(self.cert_path, exist_ok=True)
        os.makedirs(self.config_path, exist_ok=True)
        
    def _setup_cloudflare_credentials(self, credentials: Dict) -> Path:
        """Setup Cloudflare credentials file for DNS challenge"""
        cf_creds_path = Path(self.config_path) / "cloudflare.ini"
        
        with open(cf_creds_path, "w") as f:
            if "api_token" in credentials:
                f.write(f"dns_cloudflare_api_token = {credentials['api_token']}\n")
            else:
                f.write(f"dns_cloudflare_email = {credentials['email']}\n")
                f.write(f"dns_cloudflare_api_key = {credentials['api_key']}\n")
        
        # Secure the credentials file
        os.chmod(cf_creds_path, 0o600)
        return cf_creds_path

    class LetsEncryptManager(SSLManager):
        """Let's Encrypt certificate manager with Cloudflare DNS support"""
    
    def __init__(self, cert_path: str = "/etc/nginx/certs", 
                 acme_dir: str = "/etc/acme.sh",
                 staging: bool = False):
        self.cert_path = cert_path
        self.acme_dir = acme_dir
        self.staging = staging
        self._ensure_paths()
    
    def _ensure_paths(self):
        """Ensure required directories exist"""
        for path in [self.cert_path, self.acme_dir]:
            os.makedirs(path, exist_ok=True)
    
    def issue_certificate(self, domains: List[str], credentials: Dict) -> SSLCertificate:
        """
        Issue Let's Encrypt certificate with optional Cloudflare DNS challenge
        
        Args:
            domains: List of domains (can include wildcards)
            credentials: Dict containing:
                - email: Contact email for Let's Encrypt
                - cf_token: Optional Cloudflare API token for DNS challenge
                - cf_zone_id: Optional Cloudflare zone ID
        """
        try:
            email = credentials.get('email')
            cf_token = credentials.get('cf_token')
            
            if not email:
                raise ValueError("Contact email required for Let's Encrypt")

            # Check if any domain is wildcard
            has_wildcard = any('*.' in domain for domain in domains)
            
            if has_wildcard and not cf_token:
                raise ValueError("Cloudflare credentials required for wildcard certificates")

            # TODO: Implement actual certificate issuance
            # 1. Initialize ACME client
            # 2. Create/verify account
            # 3. Handle DNS or HTTP challenge
            # 4. Generate and store certificate

            return SSLCertificate(
                id=str(uuid.uuid4()),
                name=f"le-{domains[0]}",
                provider=SSLProviderType.LETSENCRYPT,
                domains=domains,
                wildcard=has_wildcard,
                challenge_type=ChallengeType.DNS if has_wildcard else ChallengeType.HTTP,
                status=CertificateStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=90),
                cloudflare_zone_id=credentials.get('cf_zone_id') if has_wildcard else None
            )

        except Exception as e:
            logging.error(f"Failed to issue Let's Encrypt certificate: {str(e)}")
            raise

    def revoke_certificate(self, cert_id: str) -> bool:
        """Revoke Let's Encrypt certificate"""
        try:
            cert = self._get_certificate(cert_id)
            if not cert:
                raise ValueError(f"Certificate {cert_id} not found")

            result = subprocess.run([
                "certbot", "revoke",
                "--cert-name", cert.name,
                "--non-interactive"
            ], capture_output=True, text=True)

            return result.returncode == 0

        except Exception as e:
            logging.error(f"Failed to revoke certificate: {str(e)}")
            return False