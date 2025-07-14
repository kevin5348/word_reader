from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
import pandas as pd
from ml.predictor import predict_difficulty_user
from deep_translator import GoogleTranslator
import asyncio
from concurrent.futures import ThreadPoolExecutor

get_difficulties_bp = Blueprint('get_difficulties', __name__)
@get_difficulties_bp.route('/get_difficulties', methods=['GET'])
@token_required

def get_difficulties(current_user_id):
    try:
        raw_words = request.args.get('words', "")
        print("Received:", raw_words)
        
        if not raw_words:
            return jsonify({"error": "No words provided"}), 400
            
        
        words = raw_words.split(",")

        from database.init_db import User
        user = User.query.filter_by(id=current_user_id).first()
        if not user: 
            return jsonify({"error": "User not found"}), 404
        user_level = user.level 
        print(f"DEBUG: User ID: {current_user_id}")      # Add this line
        print(f"DEBUG: User level: {user_level}")   

        df = pd.read_csv("datasets/data_with_predictions.csv")
        print("CSV loaded:", df.shape)

        difficulty_score = predict_difficulty_user(df, words)
        print("Prediction done")
        difficult_words = {
            word: score for word, score in difficulty_score.items() 
            if score > user_level
        }
       
    
class translator:       
        def __init__(self, source ='auto', target='es',max_workers=5):
            self.source = source
            self.target = target
            self.max_workers = max_workers    
        
        translator = GoogleTranslator(source='auto', target='es')
        translated_words ={}

        for word,score in difficult_words.items():
            try :
                translation = translator.translate(word)
                translated_words[word] = {
                    "translation": word,
                    "difficulty_score": score
                }
            except Exception as e:
                print(f"Translation error for {word}: {e}")
                translated_words[word] = {
                    "translation": word,
                    "difficulty_score": score
                    
                }
        return jsonify(difficult_words)
     
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

