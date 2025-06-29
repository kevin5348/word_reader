# server/app.py
from dotenv import load_dotenv
import os
from flask import Flask
from routes.analyze import analyze_bp
from routes.get_text import text_bp
from routes.get_difficulties import get_difficulties_bp
# from routes.user import user_bp  # (optional later)
load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# Register route blueprints
app.register_blueprint(analyze_bp, url_prefix="/analyze")
app.register_blueprint(text_bp, url_prefix="/text")
app.register_blueprint(get_difficulties_bp)
# app.register_blueprint(user_bp, url_prefix="/user")  # (optional later)
debug_mode = os.environ.get("DEBUG", "True") == "True"
if __name__ == "__main__":
    app.run(debug=debug_mode)
