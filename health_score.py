def calculate_health_score(row):

    score = 0

    if row["steps"] >= 8000:
        score += 40
    elif row["steps"] >= 5000:
        score += 25
    else:
        score += 10

    if row["heart_points"] >= 30:
        score += 30
    elif row["heart_points"] >= 10:
        score += 20
    else:
        score += 10

    if row["calories"] >= 400:
        score += 30
    else:
        score += 15

    return score
