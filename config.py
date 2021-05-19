import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    API_TOKEN = os.environ.get('API_TOKEN')
    WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')
    WEBHOOK_PORT = os.environ.get('PORT', 5000)
    WEBHOOK_URL_BASE = 'https://%s' % WEBHOOK_HOST
    WEBHOOK_URL_PATH = '/%s/' % API_TOKEN
    WEBHOOK_SSL_CERT = '../certs/cert.pem'
    UPLOAD_DIRECTORY = os.path.join(basedir, 'data')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')
