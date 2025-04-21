from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    """Load a user given the ID for Flask-Login.

    Args:
        id: The user ID to load

    Returns:
        User object or None if not found
    """
    from app.models import User

    return User.query.get(int(id))
