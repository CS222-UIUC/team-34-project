from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User
from app import db

auth = Blueprint("auth", __name__)


@auth.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=data["username"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify(user.to_dict())


@auth.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(user)
    return jsonify(user.to_dict())


@auth.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


@auth.route("/auth/user", methods=["GET"])
def get_user():
    if not current_user.is_authenticated:
        return jsonify({"error": "Not authenticated"}), 401
    return jsonify(current_user.to_dict())

@auth.route("/auth/password-reset", methods=["POST"])
def password_reset():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"error": "Email not found"}), 404

    # Generate a reset token
    token = secrets.token_hex(16)
    user.reset_token = token
    db.session.commit()

    # Send reset email
    reset_link = f"{request.host_url}auth/reset/{token}"
    msg = Message('Reset your password', recipients=[data["email"]])
    msg.body = f"Click the following link to reset your password: {reset_link}"
    mail.send(msg)

    return jsonify({"message": "Please check your email to reset your password"})
