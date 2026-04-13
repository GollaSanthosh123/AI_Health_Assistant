import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import joblib

DATA_PATH = "C:\IDP_Project/diet_recommendations_dataset.csv"
MODEL_PATH = "model.pkl"

def train_model():

    df = pd.read_csv(DATA_PATH)

    y = df["Diet_Recommendation"]

    features = [
        "Age","Gender","Weight_kg","Height_cm","BMI",
        "Disease_Type","Severity","Physical_Activity_Level",
        "Daily_Caloric_Intake","Cholesterol_mg/dL",
        "Blood_Pressure_mmHg","Glucose_mg/dL",
        "Weekly_Exercise_Hours"
    ]

    X = df[features].copy()

    encoders = {}

    for col in X.select_dtypes(include="object").columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

    target_encoder = LabelEncoder()
    y_enc = target_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="multi:softmax",
        eval_metric="mlogloss"
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print(classification_report(y_test, preds))

    bundle = {
        "model": model,
        "encoders": encoders,
        "target_encoder": target_encoder,
        "features": features
    }

    joblib.dump(bundle, MODEL_PATH)

    print("Model saved as model.pkl")


if __name__ == "__main__":
    train_model()
