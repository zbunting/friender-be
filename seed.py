"""Seed database with sample data."""

from app import app
from models import db, User, Friend, Like

app.app_context().push()

db.drop_all()
db.create_all()

test1 = User.sign_up("test_user", "password", "TestMe", "This is a bio")

db.session.commit()
