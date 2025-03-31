from flask_mail import Message
from flask import current_app
from flask_mail import Mail

mail = Mail()


def send_email(subject, recipient, heading, body):
    """Send an email using Flask-Mail."""
    try:
        msg = Message(subject=subject, recipients=[recipient])
        msg.body = f"{heading}\n\n{body}"
        msg.html = f"<h2>{heading}</h2><p>{body}</p>"
        with current_app.app_context():
            mail.send(msg)
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")
