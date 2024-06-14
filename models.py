"""SQLAlchemy models for Friender."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()

db = SQLAlchemy()
dbx = db.session.execute

DEFAULT_IMAGE_URL = "https://zb-friender.s3.amazonaws.com/default.png"


class Friend(db.Model):
    """Connection for friends"""

    __tablename__ = "friends"

    __table_args__ = (
        db.UniqueConstraint("is_friended_username", "is_friending_username"),
    )

    is_friended_username = db.mapped_column(
        db.String(25),
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )

    is_friending_username = db.mapped_column(
        db.String(25),
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )

    is_friended = db.relationship(
        "User",
        foreign_keys=[is_friended_username],
        back_populates="inc_friends",
    )

    is_friending = db.relationship(
        "User",
        foreign_keys=[is_friending_username],
        back_populates="out_friends",
    )


class Like(db.Model):
    """Connection for a like"""

    __tablename__ = "likes"

    __table_args__ = (
        db.UniqueConstraint("is_liked_username", "is_liking_username"),
    )

    # id = db.mapped_column(
    #     db.Integer,
    #     db.Identity(),
    #     primary_key=True,
    # )

    is_liked_username = db.mapped_column(
        db.String(25),
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )

    is_liking_username = db.mapped_column(
        db.String(25),
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )

    is_liked = db.relationship(
        "User",
        foreign_keys=[is_liked_username],
        back_populates="inc_likes",
    )

    is_liking = db.relationship(
        "User",
        foreign_keys=[is_liking_username],
        back_populates="out_likes",
    )


class User(db.Model):
    """An individual user"""

    __tablename__ = 'users'

    username = db.mapped_column(
        db.String(25),
        primary_key=True
    )

    hashed_pwd = db.mapped_column(
        db.String(100),
        nullable=False,
    )

    first_name = db.mapped_column(
        db.String(25),
        nullable=False,
    )

    bio = db.mapped_column(
        db.String(280),
        nullable=False,
    )

    image_url = db.mapped_column(
        db.String(100),
        nullable=False
    )

    inc_friends = db.relationship(
        "Friend",
        foreign_keys=[Friend.is_friended_username],
        back_populates="is_friended",
        cascade="all, delete-orphan"
    )

    out_friends = db.relationship(
        "Friend",
        foreign_keys=[Friend.is_friending_username],
        back_populates="is_friending",
        cascade="all, delete-orphan"
    )

    inc_likes = db.relationship(
        "Like",
        foreign_keys=[Like.is_liked_username],
        back_populates="is_liked",
        cascade="all, delete-orphan"
    )

    out_likes = db.relationship(
        "Like",
        foreign_keys=[Like.is_liking_username],
        back_populates="is_liking",
        cascade="all, delete-orphan"
    )

    @classmethod
    def sign_up(cls, username, password, first_name, bio):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            hashed_pwd=hashed_pwd,
            first_name=first_name,
            bio=bio,
            image_url=DEFAULT_IMAGE_URL
        )

        db.session.add(user)
        return user

    # add in error handling
    @property
    def user_details(self):
        """Get this user's details"""

        return {
            "username": self.username,
            "first_name": self.first_name,
            "bio": self.bio,
            "image_url": self.image_url
        }

    def update_image_url(self, image_url):
        """Change a user's image_url"""

        self.image_url = image_url
