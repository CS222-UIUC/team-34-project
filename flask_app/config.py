class Config:
    SECRET_KEY = "dev"  # Change this in production
    SQLALCHEMY_DATABASE_URI = "sqlite:///forum.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_HTTPONLY = True
