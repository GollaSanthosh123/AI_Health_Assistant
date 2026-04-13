# 🧠 AI-Driven Personalized Health and Diet Recommendation System

## 📌 Overview
This project is an AI-based health and diet recommendation system that provides personalized diet plans using machine learning and real-time health data. It integrates Google Fit to collect user activity data and generates intelligent diet recommendations along with health score analysis and future predictions.

The system aims to bridge the gap between static diet plans and dynamic, real-time health monitoring using AI.

---

## 🚀 Key Features

### 🔹 1. Machine Learning-Based Diet Prediction
- Uses **XGBoost classifier**
- Analyzes **12+ health parameters**:
  - Age, BMI, glucose, cholesterol, activity level, etc.
- Predicts personalized **diet category**

---

### 🔹 2. Google Fit Integration
- Fetches real-time user data:
  - Steps 👣
  - Heart Points ❤️
  - Calories Burned 🔥
- Uses OAuth 2.0 authentication for secure access

---

### 🔹 3. Health Score Calculation
- Computes a **health score (0–100)** based on:
  - Steps (40%)
  - Heart Points (30%)
  - Calories (30%)
- Provides quick insight into daily fitness

---

### 🔹 4. Smart Meal Recommendation
- Uses **Spoonacular API**
- Recommends meals based on:
  - Predicted diet type
  - User-provided groceries
- Generates full-day plan:
  - Breakfast 🍳
  - Lunch 🍛
  - Snack 🍎
  - Dinner 🍲

---

### 🔹 5. Data Storage (SQLite)
- Stores daily health data in **SQLite database**
- Ensures:
  - No duplicate entries
  - Efficient data retrieval
- Enables historical tracking

---

### 🔹 6. Trend Analysis & Prediction
- Visualizes **health score trends over time**
- Uses **Linear Regression** to predict future health score
- Helps users understand long-term health patterns

---

## 🛠️ Technologies Used

| Category | Tools |
|--------|------|
| Programming | Python |
| ML Model | XGBoost |
| Frontend | Streamlit |
| Data Processing | Pandas, NumPy |
| API Integration | Google Fit API, Spoonacular API |
| Database | SQLite |
| ML Libraries | Scikit-learn |

---

## 🏗️ System Architecture

User Input (Health Data) ↓ Machine Learning Model (XGBoost) ↓ Diet Prediction ↓ Google Fit API → Health Data ↓ Health Score Calculation ↓ SQLite Database (Storage) ↓ Trend Analysis + Future Prediction ↓ Meal Recommendation (API)
