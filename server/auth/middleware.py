from functools import wraps
from database.init_db import db,User
from flask import request, jsonify, current_app,g
import jwt

def token_required(f):
    """JWT decorator that validates Authorization Bearer token
    and attaches user_id to Flask global (g)"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
          

        user_id = data.get("id")
        if not user_id:
            return jsonify({"error": "Invalid token payload (missing id)"}), 401

        # Check user still exists
        user = db.session.get(User, user_id)  
        

        if not user:
            return jsonify({"error": "User not found"}), 401


        # Attach to g for querying
        g.user_id = user_id
        g.user = user

        return f(*args, **kwargs)
    
    return decorated
