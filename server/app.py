# server/app.py
from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS

load_dotenv()

def create_app():
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    # Initialize extensions with the app
    from database.init_db import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    
        # Import parts of the application
    from routes.get_difficulties import get_difficulties_bp
    from routes.login import login_bp
    from routes.refresh import refresh_bp
    from routes.get_clicks import get_clicks_bp

        # Register Blueprints
    app.register_blueprint(get_difficulties_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(refresh_bp)
    app.register_blueprint(get_clicks_bp)

    return app

app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("DEBUG", "True") == "True"
    app.run(debug=debug_mode)
