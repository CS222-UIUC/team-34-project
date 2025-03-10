Models.py from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Date

import bcrypt

import secrets

from datetime import timedelta,datetime,timezone

import csv

from io import StringIO

from sqlalchemy import JSON

from sqlalchemy.dialects.postgresql import JSONB

import base64  # Import base64 at the top of your file

 

db = SQLAlchemy()

 

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100),default="password")

    reset_token = db.Column(db.String(50), unique=True, default=None)

    reset_token_expiration = db.Column(db.DateTime, default=None)

    is_editor = db.Column(db.Boolean, default=False)  # New field for admin status

    is_admin = db.Column(db.Boolean, default=False)  # New field for admin status

    stripe_customer_id = db.Column(db.String(255), unique=True)

    subscription_status = db.Column(db.String(20), default='Free')

    email_list = db.Column(db.Boolean, default=True)  # New field for admin status

 

    def __init__(self, email, password, username):

        self.username = username

        self.email = email

        self.password = password

        self.reset_token = None

        self.reset_token_expiration = None

        self.is_editor = False

        self.is_admin = False

        self.stripe_customer_id = None  # Add this line

        self.subscription_status = "Free"  # Add this line

        self.email_list = True  # New field for admin status

    def get_id(self):

        return str(self.id)

 

    def check_password(self, password):

        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

 

    @staticmethod

    def get(user_id):

        return User.query.get(int(user_id))

 

    def generate_reset_token(self):

                self.reset_token = secrets.token_urlsafe(10)

                self.reset_token_expiration = datetime.now() + timedelta(minutes=30)

                db.session.commit()

                return self.reset_token

 

    def check_reset_token_validity(self):

                return self.reset_token_expiration > datetime.now()


    def check_password(self, password):

                return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))