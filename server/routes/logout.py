from flask import Blueprint, request, jsonify
from datetime import datetime

logout_bp = Blueprint('logout',__name__)
@logout_bp.route('/logout', methods = ['POST'])


def logout():
    data= request.get_json(force=True)
    if data.get('logged_out'):
 
        from database.init_db import User
        email = data.get('email')

        user = User.query.filter_by(email=email).first()
        if not user :
            return jsonify ({"ok":False, "error":"user not found"}), 404
        
        user_session_end(user)
        
        
        #update function
        #update server with new level and session data
        #delete clicks

        
   
        return jsonify({"ok" : True}), 200
    return jsonify({"ok":False}), 400

def user_session_end(user):
    from database.init_db import UserSession,db
   
    user_session = UserSession.query.filter_by(user_id=user.id, session_end=None).first()
    if not user_session:
            return jsonify ({"ok": True, "error" : "user session not found"}), 404
   
    user_session.session_end=datetime
    db.session.commit()