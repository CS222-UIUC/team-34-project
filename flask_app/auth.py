from flask import Blueprint, request, jsonify
from models import db, User
import bcrypt
import random
import string
from config import send_email

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# User registration route
@auth_bp.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""
    request_json = request.json
    email = request_json.get("email")
    password = request_json.get("password")
    username = request_json.get("username")

    if not email or not password or not username:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already associated with an account. Please use a different email."}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    subject = "Welcome to Fantasy Trading Room!"
    heading = "Welcome Aboard!"
    body = (
        "Welcome aboard Fantasy Trading Room! Ready to up your game? Dive into our platform "
        "for articles, tools, and rankings tailored to sports fans like you. Let's kick off your "
        "fantasy sports journey – explore now! 🚀"
    )
    send_email(subject, new_user.email, heading, body)

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "subscription_status": new_user.subscription_status,
            "is_admin": new_user.is_admin,
            "is_editor": new_user.is_editor
        }
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login_user():
    """Log in an existing user."""
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "subscription_status": user.subscription_status,
            "is_admin": user.is_admin,
            "is_editor": user.is_editor
        }
    })

@auth_bp.route("/login-google", methods=["POST"])
def login_google():
    """Log in or register a user using Google OAuth."""
    email = request.json["email"]
    username = request.json["username"]

    existing_user = User.query.filter_by(email=email).first()

    if not existing_user:
        password_length = 12
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))
        hashed_password = bcrypt.hashpw(random_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Create and save the new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Send a welcome email
        subject = "Welcome to Fantasy Trading Room!"
        heading = "Welcome Aboard!"
        body = (
            "Welcome aboard Fantasy Trading Room! Ready to up your game? Dive into our platform "
            "for articles, tools, and rankings tailored to sports fans like you. Let's kick off your "
            "fantasy sports journey – explore now! 🚀"
        )
        send_email(subject, new_user.email, heading, body)

        user = new_user
    else:
        user = existing_user

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "subscription_status": user.subscription_status,
            "is_admin": user.is_admin,
            "is_editor": user.is_editor
        }
    })

@auth_bp.route('/forgot-pass', methods=['POST'])
def forgotpass():
    """Send a password reset email to the user."""
    data = request.get_json()
    email = data.get('email')
    url = data.get('url')

    user = User.query.filter_by(email=email).first()

    if user:
        reset_token = user.generate_reset_token()
        reset_link = f"{url}/reset/{reset_token}"

        subject = "Password Reset"
        heading = "Reset Password"
        body = (
            f"We received a request to reset your password. Please click the link below to reset your password:\n\n"
            f'<a href="{reset_link}">Reset your password</a>\n\n'
            "If you did not request a password reset, please ignore this email or contact our support team."
        )
        send_email(subject, email, heading, body)

        return jsonify({'message': 'Password reset email sent. Check your inbox.'}), 200
    else:
        return jsonify({'error': 'No user found with that email address.'}), 404

@auth_bp.route('/reset/<token>', methods=['POST'])
def reset_password(token):
    """Reset the user's password using a reset token."""
    data = request.get_json()

    user = User.query.filter_by(reset_token=token).first()

    if user and user.check_reset_token_validity():
        new_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user.password = new_password
        user.reset_token = None  
        user.reset_token_expiration = None

        db.session.commit()

        return jsonify({'message': 'Password reset successful. You can now log in with your new password.'}), 200
    else:
        return jsonify({'error': 'Invalid or expired reset link.'}), 400
