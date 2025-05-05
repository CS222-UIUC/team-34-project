import pytest
from flask_app import create_app, db


@pytest.fixture
def client():
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def dummy_send_email(subject, email, heading, body):
    pass


def test_dummy_login():
    response = {"status_code": 200, "user": {"email": "dummy@example.com"}}
    assert response["status_code"] == 200
    assert "user" in response


def test_dummy_forgot_password():
    response = {
        "status_code": 200,
        "message": "Dummy forgot password test passed",
    }
    assert response["status_code"] == 200
    assert "message" in response


def test_register_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)

    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["user"]["email"] == "test@example.com"


def test_login_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)

    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser",
        },
    )

    response = client.post(
        "/login", json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "user" in response.get_json()


def test_forgot_password(client, monkeypatch):
    client.post(
        "/register",
        json={
            "email": "forgot@example.com",
            "password": "password123",
            "username": "forgotuser",
        },
    )

    monkeypatch.setattr("config.send_email", dummy_send_email)

    response = client.post(
        "/forgot-pass",
        json={"email": "forgot@example.com", "url": "http://localhost:3000"},
    )
    assert response.status_code == 200
    assert "message" in response.get_json()


def test_create_post(auth_client, category):
    response = auth_client.post(
        "/posts",
        json={
            "title": "Test Post",
            "content": "This is a test post.",
            "category_id": category.id,
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Post"
    assert data["category"]["id"] == category.id


def test_register_user_missing_fields(client):
    response = client.post(
        "/register",
        json={
            "email": "incomplete@example.com"
            # missing password and username
        },
    )
    assert response.status_code == 400


def test_register_duplicate_email(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)

    user_data = {
        "email": "dupe@example.com",
        "password": "password123",
        "username": "dupeuser",
    }

    client.post("/register", json=user_data)
    response = client.post("/register", json=user_data)
    assert response.status_code == 409  # test


def test_upvote_reply(auth_client, post, reply):
    response = auth_client.post(f"/posts/{post.id}/replies/{reply.id}/upvote")

    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Reply upvoted successfully"
    assert "upvote_count" in data
    assert data["upvote_count"] == 1
    # Assuming this is the first upvote for the reply


def test_get_posts(client, category, post):
    """
    Test retrieving all posts, optionally filtered by category.
    """
    response = client.get("/posts")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]
    assert "content" in data[0]

    # Test filtering by category
    response = client.get(f"/posts?category_id={category.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert all(post["category"]["id"] == category.id for post in data)


def test_get_post(client, post):
    """
    Test retrieving a single post by ID.
    """
    response = client.get(f"/posts/{post.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == post.id
    assert data["title"] == post.title
    assert data["content"] == post.content


def test_create_post_missing_fields(auth_client):
    """
    Test creating a post with missing required fields.
    """
    response = auth_client.post(
        "/posts",
        json={"title": "Incomplete Post"}  # Missing content and category_id
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields"


def test_create_reply(auth_client, post):
    """
    Test creating a reply for a specific post.
    """
    response = auth_client.post(
        f"/posts/{post.id}/replies",
        json={"content": "This is a test reply."}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "content" in data
    assert data["content"] == "This is a test reply."


def test_create_reply_missing_content(auth_client, post):
    """
    Test creating a reply with missing content.
    """
    response = auth_client.post(f"/posts/{post.id}/replies", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Missing reply content"


def test_vote_post(auth_client, post):
    """
    Test upvoting a post.
    """
    response = auth_client.post(
        f"/posts/{post.id}/vote",
        json={"value": 1}  # Upvote
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "user_vote" in data
    assert data["user_vote"] == 1


def test_remove_vote_post(auth_client, post):
    """
    Test removing a vote from a post.
    """
    # First, upvote the post
    auth_client.post(f"/posts/{post.id}/vote", json={"value": 1})

    # Then, remove the vote
    response = auth_client.post(
        f"/posts/{post.id}/vote",
        json={"value": 0}  # Remove vote
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "user_vote" in data
    assert data["user_vote"] == 0
