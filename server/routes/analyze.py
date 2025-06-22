from flask import Blueprint, request, jsonify
from ml.predictor import predict_difficulty

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/', methods=['POST'])
def analyze_words():
    data = request.get_json()

    if not data or "hoveredWords" not in data:
        return jsonify({"error": "Missing 'hoveredWords'"}), 400

    words = data["hoveredWords"]
    result = predict_difficulty(words)

    return jsonify(result)
