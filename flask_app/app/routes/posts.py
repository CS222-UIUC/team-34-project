from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Post, Category, Reply, PostVote, ReplyVote
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
    result = post.to_dict()
    if current_user.is_authenticated:
        result["user_vote"] = post.get_user_vote(current_user.id)
    return jsonify(result)


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


@posts.route("/posts/<int:post_id>/vote", methods=["POST"])
@login_required
def vote_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data or "value" not in data:
        return jsonify({"error": "Missing vote value"}), 400

    value = data["value"]
    if value not in [1, -1, 0]:
        return (
            jsonify(
                {
                    "error": "Invalid vote value."
                    " Must be 1 (upvote), -1 (downvote), or 0 (remove vote)"
                }
            ),
            400,
        )

    # Check if user already voted
    existing_vote = PostVote.query.filter_by(
        user_id=current_user.id, post_id=post_id
    ).first()

    if value == 0 and existing_vote:
        # Remove vote
        db.session.delete(existing_vote)
    elif existing_vote:
        # Update vote
        existing_vote.value = value
    elif value != 0:
        # Create new vote
        vote = PostVote(user_id=current_user.id, post_id=post_id, value=value)
        db.session.add(vote)

    db.session.commit()

    result = post.to_dict()
    result["user_vote"] = post.get_user_vote(current_user.id)
    return jsonify(result)


@posts.route("/replies/<int:reply_id>/vote", methods=["POST"])
@login_required
def vote_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    data = request.get_json()

    if not data or "value" not in data:
        return jsonify({"error": "Missing vote value"}), 400

    value = data["value"]
    if value not in [1, -1, 0]:
        return (
            jsonify(
                {
                    "error": "Invalid vote value."
                    " Must be 1 (upvote), -1 (downvote), or 0 (remove vote)"
                }
            ),
            400,
        )

    # Check if user already voted
    existing_vote = ReplyVote.query.filter_by(
        user_id=current_user.id, reply_id=reply_id
    ).first()

    if value == 0 and existing_vote:
        # Remove vote
        db.session.delete(existing_vote)
    elif existing_vote:
        # Update vote
        existing_vote.value = value
    elif value != 0:
        # Create new vote
        vote = ReplyVote(user_id=current_user.id,
                         reply_id=reply_id, value=value)
        db.session.add(vote)

    db.session.commit()

    result = reply.to_dict()
    result["user_vote"] = reply.get_user_vote(current_user.id)
    return jsonify(result)
