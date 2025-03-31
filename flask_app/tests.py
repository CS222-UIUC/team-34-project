import pytest
from flask import Flask
from your_package import create_app, db
from your_package.models import User

@pytest.fixture
def test_client():
    """
    This fixture creates a fresh app context and test client
    for each test to keep the database clean.
    """
    app = create_app('testing')  # Or however you configure your test environment

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register_user(test_client):
    response = test_client.post("/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Registration successful"

def test_login_user(test_client):
    # First register, then login
    test_client.post("/register", json={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "password123"
    })
    response = test_client.post("/login", json={
        "email": "loginuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
