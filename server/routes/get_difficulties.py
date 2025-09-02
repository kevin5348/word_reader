from flask import Blueprint ,request ,jsonify
from auth.middleware import token_required
import pandas as pd
from ml.predictor import predict_difficulty_user
from deep_translator import GoogleTranslator
from unicodedata import normalize
from cachetools import TTLCache
from typing import Dict,List

get_difficulties_bp = Blueprint("get_difficulties", __name__)

#cache maxsize and time until deletion
_TRANSLATION_CACHE: TTLCache = TTLCache(maxsize=20000, ttl=7*24*60*60)
_DF_CACHE = None

def csv_load():
    global _DF_CACHE
    if _DF_CACHE is None:
        _DF_CACHE = pd.read_csv("datasets/data_with_predictions.csv")
    return _DF_CACHE

#checks if input words are in cache
def cache_get(words: List[str], target: str):
    found, missing = {}, []
    for w in words:
        key = f"{target}:{w.lower()}"
        if key in _TRANSLATION_CACHE:
            found[w]= _TRANSLATION_CACHE[key]
        else:
            missing.append(w)
    return found, missing

def cache_put(translations: Dict[str, str], target : str):
    for w, t in translations.items():
        _TRANSLATION_CACHE[f"{target}:{w.lower()}"] = t

def _clean_words(words : list[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for w in words:
        if not isinstance(w, str):
            continue
        w = normalize("NFKC", w).strip()
        if not w:
            continue
        key = w.casefold()
        if key in seen :
            continue
        seen.add(key)
        out.append(w)
    return out

def chunks(words: List[str], max_words: int = 100):
    chunk = []
    for w in words:
        if len(chunk) >= max_words:
            yield chunk
            chunk = []
        chunk.append(w)
    if chunk:
        yield chunk

class Translator:
    def __init__(self, source= 'auto', target= 'es'):
        self._tr = GoogleTranslator(source=source, target=target)
        self.target = target
    
    def translate(self , words: List[str]) -> Dict[str,str]:
        words = _clean_words(words)
        if not words:
            return{}
    
        cached, missing = cache_get(words, self.target)
        result = dict(cached)

        for chunk in chunks(missing, max_words=100):
            translated_list= self._tr.translate_batch(chunk)
            batch_map = dict(zip(chunk, translated_list))
            result.update(batch_map)
            cache_put(batch_map,self.target)
        return result

@get_difficulties_bp.route('/get_difficulties', methods=['GET'])
@token_required
def get_difficulties(current_user_id):
    try:
        raw_words = request.args.get('words', "")
       
        
        if not raw_words:
            return jsonify({"error": "No words provided"}), 400
            
        words = [w.strip() for w in raw_words.split(",") if w.strip()]
        words = _clean_words(words)
        
        from database.init_db import User
        
        user = User.query.filter_by(id=current_user_id).first()
        if not user: 
            return jsonify({"error": "User not found"}), 404
        user_level = user.level 
        
  
       
        df = csv_load()    
        difficulty_score = predict_difficulty_user(df, words)
        
        
        difficult_words = {
            word: score for word, score in difficulty_score.items() 
            if score > user_level
        }
        if not difficult_words:
            return jsonify({"translations": {}})  
        
        translator = Translator(source='auto', target='es')
        translations = translator.translate(list(difficult_words.keys()))
       
        out = {
            w: {"translation": translations.get(w, w), "difficulty_score": difficult_words[w]}
            for w in difficult_words
        }   
        
        return jsonify(out)
        
    except Exception as e:
        print(f"ERROR in get_difficulties: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500