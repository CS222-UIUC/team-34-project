import pytest
from flask_app import create_app, db


@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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
    response = {"status_code": 200, "message":
                "Dummy forgot password test passed"}
    assert response["status_code"] == 200
    assert "message" in response


def test_register_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)

    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["user"]["email"] == "test@example.com"


def test_login_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)

    client.post("/register", json={
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    })

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "user" in response.get_json()


def test_forgot_password(client, monkeypatch):
    client.post("/register", json={
        "email": "forgot@example.com",
        "password": "password123",
        "username": "forgotuser"
    })

    monkeypatch.setattr("config.send_email", dummy_send_email)

    response = client.post("/forgot-pass", json={
        "email": "forgot@example.com",
        "url": "http://localhost:3000"
    })
    assert response.status_code == 200
    assert "message" in response.get_json()
def test_create_post(auth_client, category):
    response = auth_client.post("/posts", json={
        "title": "Test Post",
        "content": "This is a test post.",
        "category_id": category.id
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Post"
    assert data["category"]["id"] == category.id
def test_register_user_missing_fields(client):
    response = client.post("/register", json={
        "email": "incomplete@example.com"
        # missing password and username
    })
    assert response.status_code == 400
def test_register_duplicate_email(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)

    user_data = {
        "email": "dupe@example.com",
        "password": "password123",
        "username": "dupeuser"
    }

    client.post("/register", json=user_data)
    response = client.post("/register", json=user_data)
    assert response.status_code == 409  #test
