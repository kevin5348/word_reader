# server/app.py
from flask_cors import CORS
from flask import Flask
from routes.analyze import analyze_bp
from routes.get_text import text_bp
from routes.get_difficulties import get_difficulties_bp
# from routes.user import user_bp  # (optional later)

app = Flask(__name__)
CORS(get_difficulties_bp)
# Register route blueprints
app.register_blueprint(analyze_bp, url_prefix="/analyze")
app.register_blueprint(text_bp, url_prefix="/text")
app.register_blueprint(get_difficulties_bp)
# app.register_blueprint(user_bp, url_prefix="/user")  # (optional later)

if __name__ == "__main__":
    app.run(debug=True)
