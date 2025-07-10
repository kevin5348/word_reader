from flask import Blueprint ,request ,jsonify
import pandas as pd
from ml.predictor import predict_difficulty_user

get_difficulties_bp = Blueprint('get_difficulties', __name__)
@get_difficulties_bp.route('/get_difficulties', methods=['GET'])

def get_difficulties():
    try:
        raw_words = request.args.get("words", "")
        print("Received:", raw_words)
        words = raw_words.split(",")

        df = pd.read_csv("datasets/data_with_predictions.csv")
        print("CSV loaded:", df.shape)

        difficulty_score = predict_difficulty_user(df, words)
        print("Prediction done")

        result = {word: difficulty_score.get(word, 0.5) for word in words}
        return jsonify(result)
    
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

