from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
from typing import Dict,List
from database.init_db import ClickLog
get_clicks_bp = Blueprint("get_clicks", __name__)

@token_required
@get_clicks_bp.route('/get_clicks', methods=['GET'])
def storeClicks(wordParam: List[str]):

    



def storeNotClicked(words):
