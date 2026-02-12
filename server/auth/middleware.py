from functools import wraps
from flask import request, jsonify, current_app,g
import jwt
"""JWT token_required decorator for route protection"""
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
        
        g.user_id= data['id']

        return f(*args, **kwargs)
    
    return decorated
