from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
from datetime import datetime
from database.init_db import db, Clicked, WordDifficulty, UserSession
get_clicks_bp = Blueprint("get_clicks", __name__)

@token_required
@get_clicks_bp.route('/get_clicks', methods=['GET'])
def storeClicks():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    user_session_id= data.get('session_id')
    words_clicked=data.get('wordsClicked', [])
    words_not_clicked= data.get('wordsNotClicked', [])

    if user_session_id is None:
        return jsonify({"error": "session id required"}), 400
    
    sess = UserSession.query.filter_by(user_session_id)
    if not sess:
        return jsonify({"error" : "session not found"})
    
    now = datetime.now(datetime.timezone.utc)
    
    def add_rows(words, click_flag: bool):
       for w in words:
           wd = WordDifficulty.query.filter_by(word=w).first()
           if not wd:
               continue
           db.session.add(Clicked(
                session_id=sess.id,
                word_id=wd.id,
                clicked=click_flag,
                created_at=now
            ))
    add_rows(words_clicked)
    add_rows(words_not_clicked)
              
    db.session.commit()
    




