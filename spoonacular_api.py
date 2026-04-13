import os
import requests
import pandas as pd

SPOON_KEY = os.getenv("SPOON_KEY")

OFFLINE_PATH = "offline_food_bank.csv"

DIET_MAP = {
    "Low Carb":"low-carb",
    "High Protein":"high-protein",
    "Balanced":"balanced",
    "Diabetic":"low-sugar",
    "Heart Healthy":"low-fat"
}

def offline_fallback(diet_type, meal_type):

    df = pd.read_csv(OFFLINE_PATH)

    df = df[
        (df["diet_type"] == diet_type) &
        (df["meal_type"] == meal_type)
    ]

    return df["food_name"].tolist()[:5]


def fetch_meals(diet_type, meal_type, groceries):

    if not SPOON_KEY:
        return offline_fallback(diet_type, meal_type)

    url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        "diet": DIET_MAP.get(diet_type,"balanced"),
        "type": meal_type.lower(),
        "includeIngredients": groceries,
        "number":5,
        "apiKey":SPOON_KEY
    }

    try:

        r = requests.get(url,params=params)

        data = r.json()

        results = []

        for item in data.get("results",[]):
            results.append(item["title"])

        if results:
            return results

        return offline_fallback(diet_type, meal_type)

    except:

        return offline_fallback(diet_type, meal_type)
