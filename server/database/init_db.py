from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import Numeric
db = SQLAlchemy()
# Create users table
class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False) 
    level = db.Column(db.Float, default=0.5)
    confidence = db.Column(db.Float, default=0.0)

  

class WordDifficulty(db.Model):
    __tablename__ = 'word_difficulties'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Text, nullable=False, unique=True, index=True)
    count = db.Column(db.BigInteger, nullable=False)
    log_count = db.Column(Numeric(10, 2), nullable=False)       
    length = db.Column(db.Integer, nullable=False)
    syllables = db.Column(Numeric(5, 2), nullable=False)       
    is_homophone = db.Column(db.Boolean, nullable=False)
    pronunciation_count = db.Column(db.BigInteger, nullable=False)
    difficulty_score = db.Column(Numeric(5, 2), nullable=False) 

class Clicked(db.Model):
    __tablename__ = 'clicked'
    id = db.Column(db.Integer, primary_key = True)
    Session_id = db.Column(db.Integer,db.ForeignKey('Sessions.id', ondelete="CASCADE"),nullable= False)
    word_id = db.Column(db.Integer,db.ForeignKey('word_difficulties.id'), nullable = False)
    clicked = db.Column(db.Boolean, nullable= False)
    created_at = db.Column(db.DateTime, default=datetime)
    session = db.relationship("UserSession", back_populates="clicks")
    word = db.relationship("WordDifficulty")

class UserSession(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = False)
    session_start = db.Column(db.DateTime)
    session_end = db.Column(db.DateTime)
    total_words = db.Column(db.Integer, default = 0)
    total_clicks = db.Column(db.Integer, default = 0)
    mean_difficulty = db.Column(db.Numeric(5,2))

    clicks = db.relationship(
        "Clicked",
        back_populates="session",
        cascade = "all, delete-orphan",
        passive_deletes=True
    )





