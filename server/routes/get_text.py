from flask import Blueprint, jsonify
import os, json, random

text_bp = Blueprint('text', __name__)
BASE_TEXT_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "texts")

@text_bp.route('/<level>', methods=['GET'])
def get_text(level):
    filename = f"{level.lower()}.json"
    filepath = os.path.join(BASE_TEXT_PATH, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": f"No reading texts found for level '{level}'"}), 404

    with open(filepath, "r", encoding="utf-8") as f:
        texts = json.load(f)

    return jsonify(random.choice(texts))
