from app import db
from datetime import datetime
# Create users table
class User(db.Model):
    _tablename_='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Column(db.String(80), unique=True, nullable = False))
    hashed_password = db.Column(db.Float, default=0.5)
    level = db.Column(db.Float, default=0.5)
    confidence=db.Column(db.Float, default=0.0)

    click_logs = db.relationship('ClickLog', backref='user', lazy=True)

class ClickLog(db.Model):
    __tablename__ = 'click_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word = db.Column(db.Text, nullable=False)
    difficulty_score = db.Column(db.Float, nullable=False)
    clicked = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)