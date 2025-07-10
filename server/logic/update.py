from app import db
from database.init_db import User
from database.init_db import ClickLog

def get_last_clicks(user_id, limit=10):
    return ClickLog.query.filter_by(user_id=user_id).order_by(ClickLog.timestamp.desc()).limit(limit).all()

def update_user_level_after_clicks(user_id, confidence):    
    clicks = get_last_clicks(user_id, limit=10)
    
    # No clicks to process
    if not clicks:
        return None  
    
    elif len(clicks) > 9:
        # Calculate average difficulty score
        avg_difficulty = sum(click.difficulty_score for click in clicks) / len(clicks)

        # Fetch user's current level
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None  # User not found

         # Update level based on average difficulty and confidence
        impact = 0.05 / (1 + confidence)
        level_delta = avg_difficulty - user.level
        new_level = user.level + (impact * level_delta)
        user.level = max(0.0, min(new_level, 1.0))  # Ensure level is between 0 and 1

    
        db.session.commit()
        return user.level
    else:
        return "No sufficient clicks to update level"