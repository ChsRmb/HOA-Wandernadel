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
    enabled: bool = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, year: int, enabled: bool = True):
        self.year = year
        self.enabled = enabled

    def __repr__(self):
        return f"{self.year}"


class LocationType(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), unique=True, nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)

    def __init__(self, name: str, description: Optional[str]):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"{self.name} - {self.description}"


class Location(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    latitude: float = db.Column(db.Float, nullable=False)
    longitude: float = db.Column(db.Float, nullable=False)
    terrain_level: int = db.Column(db.Integer, nullable=False)
    difficulty_level: int = db.Column(db.Integer, nullable=False)
    image_url: Optional[str] = db.Column(db.String(255), nullable=True)
    enabled: bool = db.Column(db.Boolean, nullable=False, default=False)
    year_id: int = db.Column(db.Integer, db.ForeignKey("year.id"), nullable=False)
    year = db.relationship("Year", backref=db.backref("locations", lazy=True))
    loc_type_id: int = db.Column(db.Integer, db.ForeignKey("location_type.id"), nullable=False)
    loc_type = db.relationship("LocationType", backref=db.backref("locations", lazy=True))

    def __init__(
        self,
        name: str,
        description: Optional[str],
        latitude: float,
        longitude: float,
        terrain_level: int,
        difficulty_level: int,
        image_url: Optional[str] = None,
        enabled: bool = True,
        year=None,
        loc_type=None
    ):
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.terrain_level = terrain_level
        self.difficulty_level = difficulty_level
        self.image_url = image_url
        self.enabled = enabled
        self.year = year
        self.loc_type = loc_type

    def __repr__(self):
        return f"<Location {self.name}>"


class GeneralSettings(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    latitude: float = db.Column(db.Float, nullable=False)
    longitude: float = db.Column(db.Float, nullable=False)
    zoom_level: int = db.Column(db.Integer, nullable=False)
    marker: Optional[str] = db.Column(db.String, nullable=True)
    marker_width: Optional[int] = db.Column(db.Integer, nullable=True)
    marker_height: Optional[int] = db.Column(db.Integer, nullable=True)
    marker_anchor_x: Optional[int] = db.Column(db.Integer, nullable=True)
    marker_anchor_y: Optional[int] = db.Column(db.Integer, nullable=True)
    marker_popup_anchor_x: Optional[int] = db.Column(db.Integer, nullable=True)
    marker_popup_anchor_y: Optional[int] = db.Column(db.Integer, nullable=True)

    def __init__(
            self,
            latitude: float,
            longitude: float,
            zoom_level: int,
            marker: Optional[str] = None,
            marker_width: Optional[int] = None,
            marker_height: Optional[int] = None,
            marker_anchor_x: Optional[int] = None,
            marker_anchor_y: Optional[int] = None,
            marker_popup_anchor_x: Optional[int] = None,
            marker_popup_anchor_y: Optional[int] = None,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.zoom_level = zoom_level
        self.marker = marker
        self.marker_width = marker_width
        self.marker_height = marker_height
        self.marker_anchor_x = marker_anchor_x
        self.marker_anchor_y = marker_anchor_y
        self.marker_popup_anchor_x = marker_popup_anchor_x
        self.marker_popup_anchor_y = marker_popup_anchor_y

    def __repr__(self):
        return f"<GeneralSettings {self.id}>"
