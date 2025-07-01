from flask import Blueprint, request, jsonify
from ml.predictor import predict_difficulty_user
from logic.update import update_user_level, update_confidence
import pandas as pd 



analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/', methods=['POST'])
def analyze_words():
    data = request.get_json()

    if not data or "user_id" not in data or "interactions" not in data:
        return jsonify({"error":"Missing 'user_id' or'interactions'"}), 400

    user_id = data["user_id"]
    interactions = data["interactions"]

    if not interactions:
        return jsonify({"error":"No words provided"}), 400
    words = [item["word"] for item in interactions]
    clicked_map = {item["word"]: item.get("clicked", True) for item in interactions}

    df = pd.read_csv("server/datasets/data_with_predictions.csv")
    difficulty_score=predict_difficulty_user(df,words)

    conn = get_db_connection()
    cur = conn.cursor()
   
    for word in words:
     
        difficulty = difficulty_score.get(word, 0.5)
        clicked = clicked_map.get(word,True)

        cur.execute("""
            INSERT INTO click_logs (user_id, word, difficulty_score, clicked)
            VALUES (%s, %s ,%s, %s)
        """,(user_id,word,difficulty,clicked))
    print("DEBUG VALUES:", word, difficulty, type(difficulty), clicked)

    cur.execute("""
            SELECT word,difficulty_score, clicked
            FROM click_logs
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT 30
    """, (user_id,))
    recent_clicks = cur.fetchall()
   

    cur.execute("SELECT level, confidence FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()


    if row and isinstance(row, tuple) and len(row) == 2:
        user_level, confidence = row
    else:
        return jsonify({"error": "User not found or malformed row"}), 404

    new_level = update_user_level(recent_clicks, user_level, confidence)
    new_confidence = update_confidence(confidence, len(recent_clicks))
   
    cur.execute("""
        UPDATE users SET level = %s, confidence= %s WHERE id = %s
    """, (new_level, new_confidence, user_id))

    conn.commit()

    cur.close()
    conn.close() 
    return jsonify({"status": "success","new_level": new_level,"new_confidence": new_confidence}), 200
                   