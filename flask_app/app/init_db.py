from app import create_app
from .extensions import db
from .models import User, Category, Post, Reply, PostVote, ReplyVote


def init_db():
    app = create_app()
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create all tables
        db.create_all()

        # Create test users
        user1 = User(username="testuser")
        user1.set_password("password123")
        db.session.add(user1)

        user2 = User(username="testuser2")
        user2.set_password("password123")
        db.session.add(user2)

        user3 = User(username="testuser3")
        user3.set_password("password123")
        db.session.add(user3)

        # Create categories
        categories = [
            Category(name="General Discussion"),
            Category(name="Technical Support"),
            Category(name="Feature Requests"),
        ]
        for category in categories:
            db.session.add(category)

        db.session.commit()

        # Create sample posts
        posts = [
            Post(
                title="Welcome to the Forum",
                content=(
                    "This is our first post. "
                    "Feel free to introduce yourself!"
                ),
                user_id=user1.id,
                category_id=categories[0].id,
            ),
            Post(
                title="How to Use the Forum",
                content=(
                    "Here are some guidelines for "
                    "using the forum effectively..."
                ),
                user_id=user1.id,
                category_id=categories[0].id,
            ),
        ]
        for post in posts:
            db.session.add(post)

        db.session.commit()

        # Create sample replies
        replies = [
            Reply(
                content="Thanks for the welcome!",
                user_id=user2.id,
                post_id=posts[0].id,
            ),
            Reply(
                content="These guidelines are very helpful.",
                user_id=user3.id,
                post_id=posts[1].id,
            ),
        ]
        for reply in replies:
            db.session.add(reply)

        db.session.commit()

        # Create sample votes
        post_votes = [
            # Upvotes for first post
            PostVote(user_id=user2.id, post_id=posts[0].id, value=1),
            PostVote(user_id=user3.id, post_id=posts[0].id, value=1),
            # Mixed votes for second post
            PostVote(user_id=user2.id, post_id=posts[1].id, value=1),
            PostVote(user_id=user3.id, post_id=posts[1].id, value=-1),
        ]
        for vote in post_votes:
            db.session.add(vote)

        reply_votes = [
            # Upvotes for first reply
            ReplyVote(user_id=user1.id, reply_id=replies[0].id, value=1),
            ReplyVote(user_id=user3.id, reply_id=replies[0].id, value=1),
            # Mixed votes for second reply
            ReplyVote(user_id=user1.id, reply_id=replies[1].id, value=1),
            ReplyVote(user_id=user2.id, reply_id=replies[1].id, value=-1),
        ]
        for vote in reply_votes:
            db.session.add(vote)

        db.session.commit()

        print("Database initialized successfully with test data!")


if __name__ == "__main__":
    init_db()
