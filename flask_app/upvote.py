from app import db
from flask_login import UserMixin

'''
@posts.route("/posts/<int:post_id>/upvote", methods=["POST"])
@login_required
def upvote_post(post_id):
    post = Post.query.get_or_404(post_id)

    existing_upvote = Upvote.query.filter_by(
        user_id=current_user.id, post_id=post.id
    ).first()

    if existing_upvote:
        return jsonify({"error": "You have already upvoted this post."}), 400

    upvote = Upvote(user_id=current_user.id, post_id=post.id)
    db.session.add(upvote)
    db.session.commit()

    return (
        jsonify(
            {"message": "Post upvoted successfully", "upvote_count": len(post.upvotes)}
        ),
        201,
    )


@posts.route("/posts/<int:post_id>/replies/<int:reply_id>/upvote", methods=["POST"])
@login_required
def upvote_reply(post_id, reply_id):
    post = Post.query.get_or_404(post_id)
    reply = Reply.query.get_or_404(reply_id)

    # Check if the user has already upvoted this reply
    existing_upvote = Upvote.query.filter_by(
        user_id=current_user.id, reply_id=reply.id
    ).first()

    if existing_upvote:
        return jsonify({"error": "You have already upvoted this reply."}), 400

    # Create a new upvote
    upvote = Upvote(user_id=current_user.id, reply_id=reply.id)
    db.session.add(upvote)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Reply upvoted successfully",
                "upvote_count": len(reply.upvotes),
            }
        ),
        201,
    )
'''