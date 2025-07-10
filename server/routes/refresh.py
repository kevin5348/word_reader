from flask import Blueprint, request, jsonify, current_app
import jwt
from auth.tokens import create_token
from database.init_db import User, ClickLog

refresh_bp = Blueprint('refresh', __name__)

@refresh_bp.route('/refresh', methods=['POST'])
def refresh_token():
    token = request.json.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        id = data.get("id")
        if not id:
            return jsonify({"error": "Invalid token"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(id=id).first()  
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_token = create_token(id)
    return jsonify({"token": new_token}), 200   

