from flask import Blueprint, request, jsonify
import bcrypt
from auth.tokens import create_token

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    from database.init_db import User  # Import inside the function
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
        return jsonify({"token": token})
        
    return jsonify({"error": "Invalid credentials"}), 401