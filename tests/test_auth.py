import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import bcrypt
from flask_app import create_app, db
from datetime import datetime, timedelta

# Dummy email function to override real email sending during tests
def dummy_send_email(subject, email, heading, body):
    pass

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    # Use in‑memory SQLite database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

'''
def test_register_user(client, monkeypatch):
    # Override send_email to avoid sending real emails
    monkeypatch.setattr("config.send_email", dummy_send_email)
    
    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"

def test_register_duplicate_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)
    
    # First registration should work
    client.post("/register", json={
        "email": "dup@example.com",
        "password": "password123",
        "username": "dupuser"
    })
    # Second registration with the same email should return an error
    response = client.post("/register", json={
        "email": "dup@example.com",
        "password": "password123",
        "username": "dupuser"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_login_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)
    
    # Register a user
    client.post("/register", json={
        "email": "login@example.com",
        "password": "password123",
        "username": "loginuser"
    })
    # Successful login
    response = client.post("/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "user" in data

    # Login with a wrong password should fail
    response_fail = client.post("/login", json={
        "email": "login@example.com",
        "password": "wrongpassword"
    })
    assert response_fail.status_code == 401
    data_fail = response_fail.get_json()
    assert "error" in data_fail

def test_login_google_new_and_existing_user(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)
    
    # Test login-google for a new user (registration should occur)
    response = client.post("/login-google", json={
        "email": "google_new@example.com",
        "username": "googlenew"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "user" in data
    assert data["user"]["email"] == "google_new@example.com"
    
    # Test login-google for an existing user (should simply log in)
    response2 = client.post("/login-google", json={
        "email": "google_new@example.com",
        "username": "googlenew"
    })
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert "user" in data2
    assert data2["user"]["email"] == "google_new@example.com"

def test_forgot_password(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)
    
    # Register a user for forgot password testing
    client.post("/register", json={
        "email": "forgot@example.com",
        "password": "password123",
        "username": "forgotuser"
    })
    
    # Valid forgot-pass call
    response = client.post("/forgot-pass", json={
        "email": "forgot@example.com",
        "url": "http://localhost:3000"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data

    # Non-existent email should return 404
    response_non = client.post("/forgot-pass", json={
        "email": "nonexistent@example.com",
        "url": "http://localhost:3000"
    })
    assert response_non.status_code == 404
    data_non = response_non.get_json()
    assert "error" in data_non

def test_reset_password(client, monkeypatch):
    monkeypatch.setattr("config.send_email", dummy_send_email)
    
    # Register a user and simulate forgot password to set a reset token
    client.post("/register", json={
        "email": "reset@example.com",
        "password": "oldpassword",
        "username": "resetuser"
    })
    
    # In a real scenario, the forgot password endpoint would generate and store the token.
    # For testing, we manually set a known token and an expiration in the future.
    with client.application.app_context():
        user = User.query.filter_by(email="reset@example.com").first()
        user.reset_token = "testtoken"
        # Set an expiration time in the future (assuming your check_reset_token_validity uses this)
        user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
    
    # Attempt a password reset with the valid token
    response = client.post("/reset/testtoken", json={
        "password": "newpassword"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    
    # Verify that the new password works by logging in
    login_response = client.post("/login", json={
        "email": "reset@example.com",
        "password": "newpassword"
    })
    assert login_response.status_code == 200
    data_login = login_response.get_json()
    assert "user" in data_login

    # Attempt a reset with an invalid token should fail
    response_invalid = client.post("/reset/invalidtoken", json={
        "password": "anotherpassword"
    })
    assert response_invalid.status_code == 400
    data_invalid = response_invalid.get_json()
    assert "error" in data_invalid
'''