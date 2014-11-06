import os

class DevelopmentConfig(object):
    DATABASE_URI = 'sqlite:///app-development.db'
    DEBUG = True
    SECRET_KEY = os.environ.get('APP_SECRET_KEY', '')