import os
from dotenv import load_dotenv
import boto3
from werkzeug.utils import secure_filename

from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token
from flask import (
    Flask, request, jsonify
)

from models import (
    db, dbx, User, Friend, Like)

from sqlalchemy.exc import IntegrityError


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

jwt = JWTManager(app)
db.init_app(app)

BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
S3_LOCATION = f"http://{BUCKET_NAME}.s3.amazonaws.com/"


@app.post('/uploadimage')
def upload_image():
    """Handle image upload"""

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
    except Exception as e:
        return {"errors": str(e)}

    return {"url": f"{S3_LOCATION}{filename}"}


@app.post('/token')
def get_token():
    """Get a token"""

    # authenticate the user in model

    username = request.json["username"]

    # how to add a secret key when making the token
    token = create_access_token(identity=username)

    return jsonify({"token": token})


@app.post('/register')
def register():
    """Register user and get a token"""

    # authenticate the user in model

    username = request.json["username"]

    token = create_access_token(identity=username)

    return jsonify({"token": token})


@app.get('/users')
def get_users():
    """Get users' info"""

    decoded_token = jwt.decode(request.headers["authorization"])
    username = decoded_token["sub"]
    print(f"THE USERNAME IS -------------------->", username)

    q = db.select(User).where(User.username != username)
    usersInst = dbx(q).scalars().all()

    users = [usersInst.field for field in usersInst if field != "hashed_pwd"]

    return jsonify(users)


@app.get('/users/<username>')
def get_user(username):
    """Get user info"""

    print(f"THE RECEIVED TOKEN IS {request.headers["authorization"]}")

    # authenticate the token, in middleware?
    # in the model, query the db for the user

    # query the db (method on the user model) by username

    user = db.get_or_404(User, username)

    return jsonify({"user": user.get_user_details()})
