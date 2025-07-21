from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
import pandas as pd
from ml.predictor import predict_difficulty_user
from deep_translator import GoogleTranslator
import asyncio
from concurrent.futures import ThreadPoolExecutor

get_difficulties_bp = Blueprint('get_difficulties', __name__)

class Translator:
    def __init__(self, source='auto', target='es', max_workers=(3)):
        self.source = source
        self.target = target
        self.max_workers = max_workers    
        
    def translate_word(self, word):
        try :
            translator = GoogleTranslator(source=self.source, target=self.target)
            translation = translator.translate(word)
            return word,translation
        except Exception as e: 
            return word, word
    async def translate_words(self, words):
        if not words:
            return {}
            
        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        
            tasks = [
                loop.run_in_executor(executor, self.translate_word, word)
                for word in words
            ]
            
        
            results = await asyncio.gather(*tasks)
            
            
            return dict(results)

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
        print(f"DEBUG: User ID: {current_user_id}")     
        print(f"DEBUG: User level: {user_level}")   
       
        df = pd.read_csv("datasets/data_with_predictions.csv")
        print("CSV loaded:", df.shape)
        
        difficulty_score = predict_difficulty_user(df, words)
        print("Prediction done")
        
        difficult_words = {
            word: score for word, score in difficulty_score.items() 
            if score > user_level
        }

        print(f"Found {len(difficult_words)} difficult words")  

        if not difficult_words:
            return jsonify({"translations": {}})  
        
        translator = Translator(source='auto', target='es', max_workers=3)
        
        async def run_translation():
            return await translator.translate_words(list(difficult_words.keys()))
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            translations = loop.run_until_complete(run_translation())
        finally:
            loop.close()
            
        # Combine translations with difficulty scores
        result = {}
        for word in difficult_words:
            result[word] = {
                "translation": translations.get(word, word),
                "difficulty_score": difficult_words[word]
            }
            
        print(f"Returning {len(result)} translated words")
        return jsonify(result)
        
    except Exception as e:
        print(f"ERROR in get_difficulties: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500