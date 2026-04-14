import streamlit as st
import pandas as pd
from ml_predictor import predict_diet
from spoonacular_api import fetch_meals
from google_fit_data import fetch_health_data
from health_score import calculate_health_score
from health_prediction import predict_future_health
from database import create_table, insert_latest,fetch_data
st.markdown("""
<style>
.metric-box {
    border: 2px solid #FF4B4B;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    background-color: block;
    margin: 20px;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Diet System", layout="wide")

if "diet_type" not in st.session_state:
    st.session_state.diet_type = None

tab1, tab2, tab3 = st.tabs([
    "Health Profile",
    "Meal Planner",
    "AI HealthPredictor"
])

with tab1:

    st.header("Health Profile")

    age = st.number_input("Age",10,100,22)
    gender = st.selectbox("Gender",["Male","Female"])

    height = st.number_input("Height",120,220,170)
    weight = st.number_input("Weight",30,150,65)

    bmi = round(weight/((height/100)**2),2)

    disease = st.selectbox("Disease",
    ["None","Diabetes","Hypertension","Obesity","Heart"])

    severity = st.selectbox("Severity",
    ["Mild","Moderate","Severe"])

    activity = st.selectbox("Activity",
    ["Sedentary","Moderate","Active"])

    calories = st.number_input("Calories",1000,5000,2000)
    cholesterol = st.number_input("Cholesterol",100,400,180)
    bp = st.number_input("Blood Pressure",80,200,120)
    glucose = st.number_input("Glucose",60,300,100)
    exercise = st.number_input("Exercise Hours",0,40,5)

    if st.button("Predict Diet"):

        user_data = {
        "Age":age,
        "Gender":gender,
        "Weight_kg":weight,
        "Height_cm":height,
        "BMI":bmi,
        "Disease_Type":disease,
        "Severity":severity,
        "Physical_Activity_Level":activity,
        "Daily_Caloric_Intake":calories,
        "Cholesterol_mg/dL":cholesterol,
        "Blood_Pressure_mmHg":bp,
        "Glucose_mg/dL":glucose,
        "Weekly_Exercise_Hours":exercise
        }

        diet = predict_diet(user_data)

        st.session_state.diet_type = diet

        st.success(f"Predicted Diet: **{diet}**")

with tab2:

    if not st.session_state.diet_type:
        st.warning("Predict diet first in Tab-1")

    else:

        st.info(f"Your Diet Plan Type: **{st.session_state.diet_type}**")

        groceries = st.text_area(
            "Enter groceries you have (comma separated)",
            placeholder="egg, tomato, oats, rice"
        )

        if st.button("Generate Meal Plan"):

            meal_types = ["Breakfast","Lunch","Snack","Dinner"]

            meal_plan = {}

            for meal in meal_types:

                items = fetch_meals(
                st.session_state.diet_type,
                meal,
                groceries
                )

                if items:
                    formatted_items = "<br>".join([f"⭐ {i}" for i in items])
                else:
                    formatted_items = "➤ No meal found"

                meal_plan[meal] = formatted_items

            df = pd.DataFrame([meal_plan])

            st.subheader("Your Personalized Daily Meal Plan")
            st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
            )
                
from google_fit_data import fetch_health_data
from health_score import calculate_health_score
from health_prediction import predict_future_health
import streamlit as st

with tab3:

    st.header("Google Fit Health Dashboard")
    if st.button("Sync Google Fit Data", key="sync_btn"):

        df = fetch_health_data()

        df["health_score"] = df.apply(calculate_health_score, axis=1)
        
        latest = df.iloc[-1]
        latest["date"] = pd.to_datetime(latest["date"]).strftime("%Y-%m-%d")

        create_table()
        insert_latest(latest)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
            <h4>Steps</h4>
            <h2>{latest["steps"]}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
            <h4>Heart Points</h4>
            <h2>{latest["heart_points"]}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
            <h4>Calories</h4>
            <h2>{round(latest["calories"], 2)}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
        border: 3px solid #00C49A;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background-color: block;
        margin-top: 10px;
        ">
        <h3>Health Score</h3>
        <h1 style="color:#00C49A;">{latest["health_score"]}</h1>
        </div>
        """, unsafe_allow_html=True)
    
        st.subheader("Recent Activity")

        st.dataframe(df)

        st.subheader("Health Score Trend")
        history = fetch_data()

        if not history.empty:
            history["date"] = pd.to_datetime(history["date"])
            history = history.sort_values("date")
            history = history.set_index("date")
            st.line_chart(history["health_score"])

        else:
            st.warning("No historical data available")

        future = predict_future_health(df)
        st.success(
        f"Predicted Health Score in 3 Days: {future}"
        )
