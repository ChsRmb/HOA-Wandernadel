from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from app import db


class User(UserMixin, db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"<User {self.username}>"


class Year(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    year: int = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, year):
        self.year = year

    def __repr__(self):
        return f"{self.year}"


class Location(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    latitude: float = db.Column(db.Float, nullable=False)
    longitude: float = db.Column(db.Float, nullable=False)
    terrain_level: int = db.Column(db.Integer, nullable=False)
    difficulty_level: int = db.Column(db.Integer, nullable=False)
    image_url: Optional[str] = db.Column(db.String(255), nullable=True)
    year_id: int = db.Column(db.Integer, db.ForeignKey("year.id"), nullable=False)
    year = db.relationship("Year", backref=db.backref("locations", lazy=True))

    def __init__(
        self,
        name: str,
        description: Optional[str],
        latitude: float,
        longitude: float,
        terrain_level: int,
        difficulty_level: int,
        image_url: Optional[str] = None,
        year=None,
    ):
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.terrain_level = terrain_level
        self.difficulty_level = difficulty_level
        self.image_url = image_url
        self.year = year

    def __repr__(self):
        return f"<Location {self.name}>"
