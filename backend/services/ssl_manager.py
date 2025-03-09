from abc import ABC, abstractmethod
import os
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging
from ..data.models import SSLCertificate, SSLProviderType

class SSLManager(ABC):
    """Base SSL certificate manager"""
    
    @abstractmethod
    def issue_certificate(self, domains: List[str], credentials: Dict) -> SSLCertificate:
        """Issue new SSL certificate"""
        pass
    
    @abstractmethod
    def revoke_certificate(self, cert_id: str) -> bool:
        """Revoke existing certificate"""
        pass

class CloudflareSSL(SSLManager):
    """Cloudflare SSL certificate manager"""
    
    def __init__(self, cert_path: str = "/etc/nginx/certs"):
        self.cert_path = cert_path
        self._ensure_cert_path()
    
    def _ensure_cert_path(self):
        """Ensure certificate storage directory exists"""
        os.makedirs(self.cert_path, exist_ok=True)
    
    def issue_certificate(self, domains: List[str], credentials: Dict) -> SSLCertificate:
        """
        Issue certificate through Cloudflare
        
        Args:
            domains: List of domains for certificate
            credentials: Dict containing either:
                - api_token: Cloudflare API token
                - or:
                - email: Cloudflare account email
                - api_key: Global API key
        
        Returns:
            SSLCertificate: Newly created certificate
        """
        try:
            api_token = credentials.get('api_token')
            email = credentials.get('email')
            api_key = credentials.get('api_key')
            
            if not api_token and not (email and api_key):
                raise ValueError("Missing required Cloudflare credentials")

            # TODO: Implement Cloudflare API calls
            # 1. Verify API credentials
            # 2. Create certificate request
            # 3. Store certificate files
            
            cert = SSLCertificate(
                id=str(uuid.uuid4()),
                name=f"cf-{domains[0]}",
                provider=SSLProviderType.CLOUDFLARE,
                domains=domains,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=90)
            )
            
            return cert
            
        except Exception as e:
            logging.error(f"Failed to issue Cloudflare certificate: {str(e)}")
            raise