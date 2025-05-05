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

    reply = Reply(
        content=data["content"], user_id=current_user.id, post_id=post.id
    )

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
                    "error": (
                        "Invalid vote value. Must be 1 (upvote), "
                        "-1 (downvote), or 0 (remove vote)"
                    )
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
                    "error": (
                        "Invalid vote value. Must be 1 (upvote), "
                        "-1 (downvote), or 0 (remove vote)"
                    )
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
        vote = ReplyVote(
            user_id=current_user.id, reply_id=reply_id, value=value
        )
        db.session.add(vote)

    db.session.commit()

    result = reply.to_dict()
    result["user_vote"] = reply.get_user_vote(current_user.id)
    return jsonify(result)

'''

def get_posts_by_user(user_id):
    """
    Fetch all posts created by a specific user.
    """
    return Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all()


def delete_post(post_id):
    """
    Delete a post by its ID.
    """
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return True
    return False


def update_post_content(post_id, new_content):
    """
    Update the content of a post.
    """
    post = Post.query.get(post_id)
    if post:
        post.content = new_content
        db.session.commit()
        return post
    return None


def get_all_categories():
    """
    Fetch all available categories.
    """
    return Category.query.all()


def count_post_votes(post_id):
    """
    Count the total upvotes and downvotes for a post.
    """
    upvotes = PostVote.query.filter_by(post_id=post_id, value=1).count()
    downvotes = PostVote.query.filter_by(post_id=post_id, value=-1).count()
    return {"upvotes": upvotes, "downvotes": downvotes}


def count_replies(post_id):
    """
    Count the total number of replies for a post.
    """
    return Reply.query.filter_by(post_id=post_id).count()


def has_user_voted_on_post(user_id, post_id):
    """
    Check if a user has already voted on a specific post.
    """
    return PostVote.query.filter_by(user_id=user_id, post_id=post_id).first() is not None


def get_recent_posts(limit=10):
    """
    Fetch the most recent posts, limited by the specified number.
    """
    return Post.query.order_by(Post.timestamp.desc()).limit(limit).all()


def get_replies_for_post(post_id):
    """
    Fetch all replies for a specific post.
    """
    return Reply.query.filter_by(post_id=post_id).order_by(Reply.timestamp.asc()).all()

'''