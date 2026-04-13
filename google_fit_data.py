import pandas as pd
import time
from google_fit_service import get_fit_service

def fetch_health_data():

    service = get_fit_service()

    end = int(time.time() * 1000)
    start = end - (7 * 24 * 60 * 60 * 1000)

    body = {
    "aggregateBy":[
        {"dataTypeName":"com.google.step_count.delta"},
        {"dataTypeName":"com.google.heart_minutes"},
        {"dataTypeName":"com.google.calories.expended"}
    ],
    "bucketByTime":{"durationMillis":86400000},
    "startTimeMillis":start,
    "endTimeMillis":end
    }

    data = service.users().dataset().aggregate(
        userId="me",
        body=body
    ).execute()

    steps = []
    heart_points = []
    calories = []
    sleep = []

    from datetime import datetime

    rows = []

    for bucket in data["bucket"]:

        date = datetime.fromtimestamp(
        int(bucket["startTimeMillis"]) / 1000
        ).strftime("%Y-%m-%d")

        step_val = 0
        heart_val = 0
        cal_val = 0

        for dataset in bucket["dataset"]:
            if not dataset["point"]:
                continue

            value = dataset["point"][0]["value"][0]

            if "step_count" in dataset["dataSourceId"]:
                step_val = value.get("intVal", 0)

            elif "heart_minutes" in dataset["dataSourceId"]:
                heart_val = value.get("fpVal", 0)

            elif "calories" in dataset["dataSourceId"]:
                cal_val = value.get("fpVal", 0)

        rows.append({
        "date": date,
        "steps": step_val,
        "heart_points": heart_val,
        "calories": cal_val
        })

    df = pd.DataFrame(rows)

    return df
