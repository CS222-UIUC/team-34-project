from flask import Flask
from flask_cors import CORS
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    # Configure CORS with more detailed settings
    cors_config = {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }

    CORS(app, resources={r"/api/*": cors_config})

    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "version": "1.0.0"}

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
