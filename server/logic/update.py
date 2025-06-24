def update_user_level(recent_clicks, current_level, confidence):
    """
    Update the user level based on the distance between clicked words and current level.
    """
    
    if not recent_clicks:
        return current_level
    impact = 0.05 / (1+ confidence)

    level_delta = 0.0

    for word, difficulty, clicked in recent_clicks:
        #isolate clicked words only
        if not clicked:
            continue

        diff = difficulty - current_level
        level_delta += diff * abs(diff)

    avg_delta = level_delta / max(len(recent_clicks), 1)

    new_level = current_level + (impact * avg_delta)

    new_level = max(0.0, min(new_level, 1.0))

    return new_level

def update_confidence(confidence, total_clicks):
    """
    Increase confidence slowly with each new click.
    """
    new_confidence = confidence + (0.1 * (total_clicks / 30)) 
     # normalize to 30 clicks
    return min(new_confidence, 10.0)  