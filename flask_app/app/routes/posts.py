from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Post, Category, Reply
from app import db

posts = Blueprint("posts", __name__)


@posts.route("/posts", methods=["GET"])
def get_posts():
    category_id = request.args.get("category_id", type=int)
    query = Post.query.order_by(Post.timestamp.desc())

    if category_id:
        query = query.filter_by(category_id=category_id)

    posts = query.all()
    return jsonify([post.to_dict() for post in posts])


@posts.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@posts.route("/posts", methods=["POST"])
@login_required
def create_post():
    data = request.get_json()

    if (
        not data
        or "title" not in data
        or "content" not in data
        or "category_id" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Invalid category"}), 400

    post = Post(
        title=data["title"],
        content=data["content"],
        category_id=data["category_id"],
        user_id=current_user.id,
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201


@posts.route("/posts/<int:post_id>/replies", methods=["POST"])
@login_required
def create_reply(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data or "content" not in data:
        return jsonify({"error": "Missing content"}), 400

    reply = Reply(content=data["content"],
                  user_id=current_user.id, post_id=post.id)

    db.session.add(reply)
    db.session.commit()

    return jsonify(reply.to_dict()), 201
