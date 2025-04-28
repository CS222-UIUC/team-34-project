from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(UserMixin, BaseModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    replies = db.relationship("Reply", backref="author", lazy="dynamic")
    post_votes = db.relationship("PostVote", backref="user", lazy="dynamic")
    reply_votes = db.relationship("ReplyVote", backref="user", lazy="dynamic")

    def set_password(self, password: str) -> None:
        """Hashes and sets the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username}

    def __repr__(self):
        return f"<User {self.username}>"


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship("Post", backref="category", lazy="dynamic")

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f"<Category {self.name}>"

    def __str__(self) -> str:
        """String representation of Category."""
        return self.name


class PostVote(db.Model):
    __tablename__ = "post_vote"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    # 1 for upvote, -1 for downvote
    value = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "post_id", name="uq_post_vote_user_post"
        ),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
        }


class ReplyVote(db.Model):
    __tablename__ = "reply_vote"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey("reply.id"), nullable=False)
    value = db.Column(
        db.Integer, nullable=False
    )  # 1 for upvote, -1 for downvote
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "reply_id", name="uq_reply_vote_user_reply"
        ),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "reply_id": self.reply_id,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
        }


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    replies = db.relationship("Reply", backref="post", lazy="dynamic")
    votes = db.relationship("PostVote", backref="post", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "category_id": self.category_id,
            "author": self.author.to_dict() if self.author else None,
            "category": self.category.to_dict() if self.category else None,
            "replies": [reply.to_dict() for reply in self.replies],
            "vote_count": self.vote_count,
        }

    def __repr__(self):
        return f"<Post {self.title}>"

    @property
    def is_empty(self) -> bool:
        """Check if post has no content."""
        return not bool(self.content.strip())

    @property
    def reply_count(self) -> int:
        """Get number of replies to this post."""
        return self.replies.count()

    @property
    def vote_count(self) -> int:
        """Get vote count (upvotes minus downvotes)"""
        from sqlalchemy import func

        result = (
            db.session.query(func.sum(PostVote.value))
            .filter(PostVote.post_id == self.id)
            .scalar()
        )
        return result or 0

    def get_user_vote(self, user_id) -> int:
        """Get the value of a user's vote for this post.

        Returns:
            1 for upvote, -1 for downvote, or 0 if no vote
        """
        vote = PostVote.query.filter_by(
            post_id=self.id, user_id=user_id
        ).first()
        return vote.value if vote else 0

    def __str__(self) -> str:
        """String representation of Post."""
        return f"{self.title} by {self.author.username}"


class Reply(db.Model):
    __tablename__ = "reply"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    votes = db.relationship("ReplyVote", backref="reply", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id,
            "author": self.author.to_dict() if self.author else None,
            "vote_count": self.vote_count,
        }

    def __repr__(self):
        return f"<Reply {self.id} on Post {self.post_id}>"

    @property
    def vote_count(self) -> int:
        """Get vote count (upvotes minus downvotes)"""
        from sqlalchemy import func

        result = (
            db.session.query(func.sum(ReplyVote.value))
            .filter(ReplyVote.reply_id == self.id)
            .scalar()
        )
        return result or 0

    def get_user_vote(self, user_id) -> int:
        """Get the value of a user's vote for this reply.

        Returns:
            1 for upvote, -1 for downvote, or 0 if no vote
        """
        vote = ReplyVote.query.filter_by(
            reply_id=self.id, user_id=user_id
        ).first()
        return vote.value if vote else 0
