from flask import Blueprint, request, jsonify,g
from auth.middleware import token_required
from datetime import datetime
from logic.update import update_user_level_after_clicks
logout_bp = Blueprint('logout',__name__)
@logout_bp.route('/logout', methods = ['POST'])

@token_required
def logout():
    data= request.get_json(force=True)
    if data.get('logged_out'):
 
        

        user = g.user_id
        if not user :
            return jsonify ({"ok":False, "error":"user not found"}), 404
        
        update_user_level_after_clicks()
        user_session_end(user)
   
        return jsonify({"ok" : True}), 200
    return jsonify({"ok":False}), 400

def user_session_end(user):
    from database.init_db import UserSession,db
   
    user_session = UserSession.query.filter_by(user_id=user, session_end=None).first()
    if not user_session:
            return jsonify ({"ok": True, "error" : "user session not found"}), 404
    session = UserSession.query.filter_by(user_id=user).first()


    
    user_session.session_end=datetime
    db.session.delete(session)
    db.session.commit()
