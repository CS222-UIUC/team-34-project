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
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

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
