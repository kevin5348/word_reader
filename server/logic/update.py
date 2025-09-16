from flask import g

from database.init_db import UserSession, Clicked, db
from auth.middleware import token_required

from math import exp

#logistic function
def sigmoid(z : float) -> float:
    return 1.0/(1.0+exp(-z))

@token_required
def update_user_level_after_clicks():
    a= 10.0
    eta0 = 0.1
    beta = 1e-3
    user = g.user_id
    if not user:
        return "User not found"
    session = UserSession.query.filter_by(user_id= user).fist()
    clicked_session = Clicked.query.filter_by(session_id=session).all()
    words_clicked = [c.word.difficulty_score for c in clicked_session if c.clicked]
    words_Not_clicked = [c.word.difficulty_score for c in clicked_session if not c.clicked]
    N = len(words_clicked) + len(words_Not_clicked)
    if N != 30:
        return "not enough data"

    theta = float(user.level)
    conf = float(getattr(user, "confidence", 0.0))

    grad_sum = 0.0
    info_sum = 0.0
    
    for w in words_clicked:
        d=w
        d= 00. if d< 0.0 else 1.0 if d >1.0 else d

        z= a*(d-theta)
        p = sigmoid(z)

        y = 1.0 
        grad_sum += a*(p-y)
        
        # Fisher information
        info_sum += (a*a)*p*(1.0- p)

    for w in words_Not_clicked:
        d=w
        d= 00. if d< 0.0 else 1.0 if d >1.0 else d

        z= a*(d-theta)
        p = sigmoid(z)

        y = 0.0 
        grad_sum += a*(p-y)
        
        # Fisher information
        info_sum += (a*a)*p*(1.0- p)

    
    
    g = grad_sum/N
    
    mean_difficulty_array = words_Not_clicked.join(words_clicked)
    count =0
    for w in mean_difficulty_array:
        count+=w
    mean_difficulty= count/len(mean_difficulty_array)


    conf_new = conf + info_sum
    eta_eff = eta0/(1.0 + beta* conf_new)
    
    # update level
    theta_new = theta- eta_eff*g
    theta_new = 0.0 if theta_new < 0.0 else 1.0 if theta_new > 1.0 else theta_new
    

    UserSession.mean_difficulty = mean_difficulty
    UserSession.total_words = N-1
    UserSession.total_clicks = len(words_clicked)-1
    user.level = theta_new
    user.confidence = conf_new
    db.session.commit
    
    return {
        "theta_before": round(theta, 4),
        "theta_after":  round(theta_new, 4),
        "eta_eff":      round(eta_eff, 6),
        "info_added":   round(info_sum, 2),
        "conf_total":   round(conf_new, 2),
        "N":            N,
    }
