from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
get_clicks_bp = Blueprint("get_clicks", __name__)

@token_required
def storeClicks():
    

