import jwt
from database.init_db import User
import datetime
from flask import Blueprint ,request ,jsonify
import bcrypt
import os

login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['POST'])
def create_token():
    payload = {
        "id" :id,
        "exp": datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, os.environ.get("SECRET_KEY"),algorithm=os.environ.get("ALGO"))

def login():
    data= request.json
    email= data.get("email")
    password = data.get(password).encode('utf-8')
    #filters database for specific user
    user = User.query.filter_by(username=email).first()
    #checks if user has correct password user tokens
    if user and bcrypt.checkpw(password, user[1].encode('utf-8')):
        token = create_token(user[0])
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}),401