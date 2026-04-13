import joblib
import pandas as pd

MODEL_PATH = "model.pkl"

bundle = joblib.load(MODEL_PATH)

model = bundle["model"]
encoders = bundle["encoders"]
target_encoder = bundle["target_encoder"]
features = bundle["features"]

def predict_diet(user_data):

    df = pd.DataFrame([user_data])[features]

    for col, le in encoders.items():
        try:
            df[col] = le.transform(df[col].astype(str))
        except:
            df[col] = 0

    pred = model.predict(df)[0]

    diet = target_encoder.inverse_transform([pred])[0]

    return diet
