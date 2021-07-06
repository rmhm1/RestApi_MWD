from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_LINK')


class DevConfig(Config):
    SECRET_KEY = environ.get('DEV_SECRET_KEY')
    DEBUG = True


class ProdConfig(Config):
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = False


config_by_name = dict(
    base=Config,
    dev=DevConfig,
    prod=ProdConfig
)
