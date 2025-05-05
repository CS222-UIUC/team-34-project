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

        # Create test users with more descriptive usernames
        test_users = [
            {"username": "SportsFanatic", "password": "password123"},
            {"username": "TeamCaptain", "password": "password123"},
            {"username": "StatsGuru", "password": "password123"},
        ]

        users = []
        for user_data in test_users:
            user = User(username=user_data["username"])
            user.set_password(user_data["password"])
            db.session.add(user)
            users.append(user)

        # Create categories with descriptions
        category_data = [
            {
                "name": "Match Discussions",
                "description": "Live and post-match discussions"
            },
            {
                "name": "Analysis & Stats",
                "description": "Deep dives into sports statistics"
            },
            {
                "name": "Breaking News",
                "description": "Latest sports updates and transfers"
            },
        ]

        categories = []
        for cat in category_data:
            category = Category(name=cat["name"])
            db.session.add(category)
            categories.append(category)

        db.session.commit()

        # Create sample posts
        posts = [
            Post(
                title="Welcome to the Forum",
                content=(
                    "This is our first post. "
                    "Feel free to introduce yourself!"
                ),
                user_id=users[0].id,
                category_id=categories[0].id,
            ),
            Post(
                title="How to Use the Forum",
                content=(
                    "Here are some guidelines for "
                    "using the forum effectively..."
                ),
                user_id=users[0].id,
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
                user_id=users[1].id,
                post_id=posts[0].id,
            ),
            Reply(
                content="These guidelines are very helpful.",
                user_id=users[2].id,
                post_id=posts[1].id,
            ),
        ]
        for reply in replies:
            db.session.add(reply)

        db.session.commit()

        # Create sample votes
        post_votes = [
            # Upvotes for first post
            PostVote(user_id=users[1].id, post_id=posts[0].id, value=1),
            PostVote(user_id=users[2].id, post_id=posts[0].id, value=1),
            # Mixed votes for second post
            PostVote(user_id=users[1].id, post_id=posts[1].id, value=1),
            PostVote(user_id=users[2].id, post_id=posts[1].id, value=-1),
        ]
        for vote in post_votes:
            db.session.add(vote)

        reply_votes = [
            # Upvotes for first reply
            ReplyVote(user_id=users[0].id, reply_id=replies[0].id, value=1),
            ReplyVote(user_id=users[2].id, reply_id=replies[0].id, value=1),
            # Mixed votes for second reply
            ReplyVote(user_id=users[0].id, reply_id=replies[1].id, value=1),
            ReplyVote(user_id=users[1].id, reply_id=replies[1].id, value=-1),
        ]
        for vote in reply_votes:
            db.session.add(vote)

        db.session.commit()

        print("Database initialized successfully with test data!")


if __name__ == "__main__":
    init_db()
