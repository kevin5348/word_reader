# server/auth/tokens.py
import jwt
import datetime
from flask import current_app

def create_token(user_id):
    """Creates a JWT token for a given user ID."""
    payload = {
        "id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    token = jwt.encode(
        payload, 
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return token
