import sqlite3
import pandas as pd

DB_NAME = "health.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS health_data (
        date TEXT UNIQUE,
        steps INTEGER,
        heart_points REAL,
        calories REAL,
        health_score REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_data(date, steps, heart_points, calories, health_score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # prevent duplicate (same date)
    c.execute("""
    INSERT OR REPLACE INTO health_data VALUES (?, ?, ?, ?, ?)
    """, (date, steps, heart_points, calories, health_score))

    conn.commit()
    conn.close()
def insert_dataframe(df):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for _, row in df.iterrows():
        c.execute("""
        INSERT OR REPLACE INTO health_data
        (date, steps, heart_points, calories, health_score)
        VALUES (?, ?, ?, ?, ?)
        """, (
            row["date"],
            int(row["steps"]),
            float(row["heart_points"]),
            float(row["calories"]),
            float(row["health_score"])
        ))

    conn.commit()
    conn.close()
def insert_latest(row):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 🔥 DELETE old entry of same date
    c.execute("DELETE FROM health_data WHERE date = ?", (row["date"],))

    # 🔥 INSERT fresh
    c.execute("""
    INSERT INTO health_data (date, steps, heart_points, calories, health_score)
    VALUES (?, ?, ?, ?, ?)
    """, (
        row["date"],
        int(row["steps"]),
        float(row["heart_points"]),
        float(row["calories"]),
        float(row["health_score"])
    ))

    conn.commit()
    conn.close()
def fetch_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM health_data", conn)
    conn.close()
    return df
