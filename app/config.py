from os import environ, path
from dotenv import load_dotenv, find_dotenv

# Loads the .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(find_dotenv())


# Base Configuration
class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_LINK')

# Development configuration
class DevConfig(Config):
    SECRET_KEY = environ.get('DEV_SECRET_KEY')
    DEBUG = True


# Production Configuration
class ProdConfig(Config):
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = False


# Dictionary of possible configurations for easy retrieval
config_by_name = dict(
    base=Config,
    dev=DevConfig,
    prod=ProdConfig
)
