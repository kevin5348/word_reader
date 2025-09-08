from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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

    click_logs = db.relationship('ClickLog', backref='user', lazy=True)

class ClickLog(db.Model):    
    __tablename__ = 'click_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word = db.Column(db.Text, nullable=False)
    difficulty_score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime)

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
    __tablename__ = 'Clicked'
    id = db.column(db.Integer, primary_key = True)
    Session_id = db.Column(db.String,db.ForeignKey('session.id', ondelete="CASCADE"),nullable= False)
    #add word id link to word diff and get diff for word link to the id
    word_id = db.column(db.Text, nullable = False)
    clicked = db.column(db.boolean, nullable= False)


class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.column(db.Integer, primary_key= True)
    user_id = db.column(db.Integer,db.Foreign_key('users.id'), nullable = False)
    session_start = db.column(db.DateTime)
    session_end = db.column(db.DateTime)
    total_words = db.column(db.Integer, default = 0)
    total_clicks = db.column(db.Integer, default = 0)
    mean_difficulty = db.Column(db.Numeric(5,2))

    clicks = db.relationship(
        "Clicked",
        back_populates="session",
        cascade = "all, delete-orphan"
        passive_deletes=True
    )





