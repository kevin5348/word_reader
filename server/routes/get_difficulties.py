from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
import pandas as pd
from ml.predictor import predict_difficulty_user

get_difficulties_bp = Blueprint('get_difficulties', __name__)
@get_difficulties_bp.route('/get_difficulties', methods=['GET'])
@token_required

def get_difficulties(current_user_id):
    try:
        raw_words = request.args.get("words", "")
        print("Received:", raw_words)
        words = raw_words.split(",")

        from database.init_db import User
        user = User.query.filter(id=current_user_id).first()
        if not user: jsonify({"error": "User not found"}), 404
        user_level = user.level 

        df = pd.read_csv("datasets/data_with_predictions.csv")
        print("CSV loaded:", df.shape)

        difficulty_score = predict_difficulty_user(df, words)
        print("Prediction done")
        difficult_words = {
            word: score for word, score in difficulty_score.items() 
            if score < user_level
        }
        
        return difficult_words
    
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

