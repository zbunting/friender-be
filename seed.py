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

like1 = Like(is_liked_username=test1.username,
             is_liking_username=test4.username)
like2 = Like(is_liked_username=test1.username,
             is_liking_username=test2.username)
db.session.add(like1)
db.session.add(like2)

friend1 = Friend(is_friended_username=test1.username,
                 is_friending_username=test2.username)
db.session.add(friend1)

db.session.commit()
