def calculate_health_score(row):

    score = 0

    # Steps score
    if row["steps"] >= 8000:
        score += 50
    elif row["steps"] >= 5000:
        score += 30
    else:
        score += 10

    # Heart rate score
    if 60 <= row["heart_rate"] <= 100:
        score += 50
    else:
        score += 25

    return score
