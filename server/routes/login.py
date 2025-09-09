from flask import Blueprint, request, jsonify
import bcrypt
from auth.tokens import create_token

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    from database.init_db import User 
    session_start = False 
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # filters database for specific user by email
    user = User.query.filter_by(email=email).first()

    # checks if user exists and if the password is correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        token = create_token(user.id)
        session_start = True
        return jsonify({"token": token}) 
    # log users session
    if session_start:
        start_session(user)            
    return jsonify({"error": "Invalid credentials"}), 401

def start_session(user):
    from database.init_db import UserSession, db
    from datetime import datetime
    session = UserSession.query.filter_by(user_id=user.id).first()
    if session:
        return session
    
    new_session= UserSession(
        user_id = user.id,
        session_start = datetime
    )

    db.session.add(new_session)
    db.session.commit()