import os
from dotenv import load_dotenv
import boto3
from werkzeug.utils import secure_filename

from flask_cors import CORS

import jwt
# from flask_jwt_extended import JWTManager, create_access_token
from flask import (
    Flask, request, jsonify
)

from models import (
    db, dbx, User, Friend, Like)

from sqlalchemy import and_, or_


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

cors = CORS(app)
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# jwt = JWTManager(app)
db.init_app(app)

BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
S3_LOCATION = f"http://{BUCKET_NAME}.s3.amazonaws.com/"
SECRET_KEY = os.environ['SECRET_KEY']


@app.post('/uploadimage')
def upload_image():
    """Handle image upload"""

    decoded_token = jwt.decode(
        request.headers["authorization"], SECRET_KEY, algorithms=['HS256'])

    username = decoded_token["username"]
    user = db.get_or_404(User, username)

    # need to validate file type
    # WTForms?
    file = request.files['image']

    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            filename,
            ExtraArgs={
                "ContentType": file.content_type,
            }
        )
        user.update_image_url(f"{S3_LOCATION}{filename}")
        db.session.commit()
    except Exception as e:
        return {"errors": str(e)}

    return {"url": f"{S3_LOCATION}{filename}"}


@app.post('/token')
def get_token():
    """Get a token"""

    # authenticate the user in model

    username = request.json["username"]

    # how to add a secret key when making the token
    token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


@app.post('/register')
def register():
    """Register user and get a token"""

    # authenticate the user in model

    username = request.json["username"]

    token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


@app.get('/users')
def get_users():
    """Get users' info"""

    decoded_token = jwt.decode(
        request.headers["authorization"], SECRET_KEY, algorithms=['HS256'])

    curr_username = decoded_token["username"]

    q = (
        db.select(User)
        .outerjoin(Like, Like.is_liking_username == User.username)
        .outerjoin(Friend, Friend.is_friending_username == User.username)
        .where(
            and_(
                User.username != curr_username,
                or_(
                    and_(
                        Friend.is_friending_username != curr_username,
                        Friend.is_friended_username != curr_username,
                        Like.is_liking_username != curr_username
                    ),
                    Like.is_liking_username.is_(None),
                    and_(
                        Like.is_liking_username != curr_username,
                        Friend.is_friending_username.is_(None)
                    )
                )
            )
        )
    )

    print(f"THE QUERY IS ------------------->", q)

    usersInst = dbx(q).scalars().all()
    print(f"THE USERS ARE -------------------->", usersInst)

    users = [user.user_details for user in usersInst]

    return jsonify({"users": users})


@app.get('/users/<username>')
def get_user(username):
    """Get user info"""

    print(f"THE RECEIVED TOKEN IS {request.headers["authorization"]}")

    # authenticate the token, in middleware?
    # in the model, query the db for the user

    # query the db (method on the user model) by username

    user = db.get_or_404(User, username)

    return jsonify({"user": user.user_details})


@app.get('/users/<username>/friends')
def get_friends(username):
    """Get a user's friends"""

    decoded_token = jwt.decode(
        request.headers["authorization"], SECRET_KEY, algorithms=['HS256'])

    curr_username = decoded_token["username"]

    q = (
        db.select(User)
        .join(Friend, Friend.is_friending_username == User.username)
        .where(
            or_(
                Friend.is_friending_username == curr_username,
                Friend.is_friended_username == curr_username,
            )
        )
    )

    usersInst = dbx(q).scalars().all()
    print(f"THE USERS ARE -------------------->", usersInst)

    users = [user.user_details for user in usersInst]

    return jsonify({"users": users})


@app.post('/users/like/<username>')
def like_user(username):
    """Like a user"""

    decoded_token = jwt.decode(
        request.headers["authorization"], SECRET_KEY, algorithms=['HS256'])

    curr_username = decoded_token["username"]

    # query the db to see if username has liked curr user
    q = db.select(Like).where(Like.is_liking_username == username and
                              Like.is_liked_username == curr_username)
    like = dbx(q).one_or_none()

    if (like):
        friend = Friend(is_friended_username=curr_username,
                        is_friending_username=username)
        db.session.add(friend)
        db.session.commit()
        return jsonify({"msg": "match"})

    new_like = Like(is_liked_username=username,
                    is_liking_username=curr_username)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({"msg": "liked"})
