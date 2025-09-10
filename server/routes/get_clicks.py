from flask import Blueprint ,request ,jsonify,g
from auth.middleware import token_required
from datetime import datetime, timezone
from database.init_db import db, Clicked, WordDifficulty, UserSession
get_clicks_bp = Blueprint("get_clicks", __name__)


@get_clicks_bp.route('/get_clicks', methods=['POST'])
@token_required
def storeClicks():
    
    data = request.get_json(silent=True) or {}
   
    user_id = g.user_id
    if not user_id:
      return jsonify({"error" : "user id required"}),404
    user_session= UserSession.query.filter_by(user_id=user_id, session_end= None).first()
    
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    words_clicked=data.get('wordsClicked', [])
    words_not_clicked= data.get('wordsNotClicked', [])

    if user_session is None:
        return jsonify({"error": "session id required"}), 400
    
    sess = user_session.id
    if not sess:
        return jsonify({"error" : "session not found"})
    
    now = datetime.now(timezone.utc)
    
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
    return '', 204
    





