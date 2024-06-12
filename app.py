import os
from dotenv import load_dotenv
import boto3
from werkzeug.utils import secure_filename

from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token
from flask import (
    Flask, request, jsonify
)

# from models import (
#     db, dbx)

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
# s3 = boto3.resource('s3')
jwt = JWTManager(app)
# db.init_app(app)

BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
S3_LOCATION = f"http://{BUCKET_NAME}.s3.amazonaws.com/"

# put the below in a .env file (no quotes for AWS info)
# SECRET_KEY="something""
# DATABASE_URL="//"
# AWS_ACCESS_KEY=
# AWS_SECRET_ACCESS_KEY=
# AWS_BUCKET_NAME=
# AWS_DOMAIN=http://bucket_name.s3.amazonaws.com/


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


@app.post('/users/<username>')
def get_user(username):
    """Get user info"""

    # authenticate the token, in middleware?
    # in the model, query the db for the user

    return jsonify({"user": {username: "testuser"}})
