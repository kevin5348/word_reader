from flask import Blueprint ,request ,jsonify
import pandas as pd
from ml.predictor import predict_difficulty_user

get_difficulties_bp = Blueprint('get_difficulties', __name__)
@get_difficulties_bp.route('/get_difficulties', methods=['GET'])

def get_difficulties():
    user_id = request.args.get("user_id")
    words = request.args.get("words", "").split(",")

    df = pd.read_csv("server/datasets/data_with_predictions.csv")
    difficulty_score = predict_difficulty_user(df, words)
    
    result = {word: difficulty_score.get(word, 0.5) for word in words}
    return jsonify(result)
