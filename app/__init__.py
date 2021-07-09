import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_by_name
from sqlalchemy import create_engine

db = SQLAlchemy()
engine = create_engine(os.environ.get('DATABASE_LINK'))


# Creates and returns the app with a specific configuration
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        return app
