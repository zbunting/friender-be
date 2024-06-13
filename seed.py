"""Seed database with sample data."""

from app import app
from models import db, User, Friend, Like

app.app_context().push()

db.drop_all()
db.create_all()

test1 = User.sign_up("test_user", "password", "TestMe", "This is a bio")
test2 = User.sign_up("test_user2", "password", "TestMe2", "This is a bio2")
test3 = User.sign_up("test_user3", "password", "TestMe3", "This is a bio3")
test4 = User.sign_up("test_user4", "password", "TestMe4", "This is a bio4")

db.session.commit()
