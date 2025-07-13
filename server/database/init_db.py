from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
# Create users table
class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False) 
    level = db.Column(db.Float, default=0.5)
    confidence = db.Column(db.Float, default=0.0)
    
    
    click_logs = db.relationship('ClickLog', backref='user', lazy=True)

class ClickLog(db.Model):    
    __tablename__ = 'click_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word = db.Column(db.Text, nullable=False)
    difficulty_score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)