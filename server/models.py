# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan"
    )

    # Many-to-many convenience relationship via appearances
    guests = db.relationship(
        "Guest",
        secondary="appearances",
        viewonly=True,
        back_populates="episodes"
    )

    # Prevent infinite recursion
    serialize_rules = (
        "-appearances.episode",
        "-guests.episodes",
    )


class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

    episodes = db.relationship(
        "Episode",
        secondary="appearances",
        viewonly=True,
        back_populates="guests"
    )

    serialize_rules = (
        "-appearances.guest",
        "-episodes.guests",
    )


class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(
        db.Integer,
        db.ForeignKey("episodes.id"),
        nullable=False
    )
    guest_id = db.Column(
        db.Integer,
        db.ForeignKey("guests.id"),
        nullable=False
    )

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # Avoid recursion
    serialize_rules = (
        "-guest.appearances",
        "-episode.appearances",
    )

    @validates("rating")
    def validate_rating(self, key, value):
        if value is None:
            raise ValueError("Rating is required")
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
