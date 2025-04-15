from flask import Flask
from flask_cors import CORS
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    # Configure CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "http://localhost:3000",
                "supports_credentials": True,
            }
        },
    )

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .routes import main, auth, posts, categories

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(posts, url_prefix="/api")
    app.register_blueprint(categories, url_prefix="/api")

    return app
