from flask import Blueprint, jsonify
import os, json, random


text_bp = Blueprint('text', __name__)
TEXT_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "texts", "english_level.json")

@text_bp.route('/<level>', methods=['GET'])
def get_text(level):
    if not os.path.exists(TEXT_PATH):
        return jsonify({"error": "Text database not found."}), 404

    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        all_texts = json.load(f)

    filtered = [entry for entry in all_texts if entry["id"].lower().startswith(level.lower())]

    if not filtered:
        return jsonify({"error": f"No reading texts found for level '{level}'"}), 404

    return jsonify(filtered)
