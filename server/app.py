# server/app.py
from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)

    with app.app_context():
        # Import parts of our application
        from routes.get_difficulties import get_difficulties_bp
        from routes.login import login_bp
        from routes.refresh import refresh_bp

        # Register Blueprints
        app.register_blueprint(get_difficulties_bp)
        app.register_blueprint(login_bp)
        app.register_blueprint(refresh_bp)

        # Add a command to initialize the database
        @app.cli.command("init-db")
        def init_db_command():
            """Clear existing data and create new tables."""
            db.create_all()
            print("Initialized the database.")

    return app

app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("DEBUG", "True") == "True"
    app.run(debug=debug_mode)
