# server/app.py
from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from routes.get_text import text_bp
#from routes.get_difficulties import get_difficulties_bp

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE']=os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
# Register route blueprints

#app.register_blueprint(text_bp, url_prefix="/text")
#app.register_blueprint(get_difficulties_bp)

debug_mode = os.environ.get("DEBUG", "True") == "True"
if __name__ == "__main__":
    app.run(debug=debug_mode)
