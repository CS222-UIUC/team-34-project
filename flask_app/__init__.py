from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .auth import auth_bp  # assuming auth.py is where all your routes live
from .config import Config  # or import based on your config setup

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # You can add more config profiles here if needed
    if config_name == 'testing':
        app.config.from_mapping(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            SECRET_KEY='test',
        )
    else:
        app.config.from_object(Config)

    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)

    return app
