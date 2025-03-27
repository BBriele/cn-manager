import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-need-a-secret-key'
    # Add other configuration variables here (e.g., Cloudflare API key)