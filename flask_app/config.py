import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'   # Use your SMTP server (Gmail, Outlook, etc.)
    MAIL_PORT = 587                   # TLS Port (Use 465 for SSL)
    MAIL_USE_TLS = True                # Enable Transport Security Layer
    MAIL_USE_SSL = False               # Disable SSL if using TLS
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Email address
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # App password (not actual email password)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")  # Default sender email
