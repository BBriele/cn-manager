import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-need-a-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@host:port/database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PATH_TO_PROJ_CERT = os.environ.get('PATH_TO_PROJ_CERT', '/path/to/certs')