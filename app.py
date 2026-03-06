import streamlit as st
import pandas as pd
import random
from database.db import fetch_data, create_table, insert_data
from utils.gemini_analyzer import analyze_vitals

st.set_page_config(page_title="AI Healthcare Monitor", layout="wide")

st.title("🧠 Gemini AI Healthcare Monitoring Dashboard")

# make sure the monitoring table exists
create_table()

def generate_dummy(n=5):
    """Insert a few random records for testing/demo."""
    for _ in range(n):
        vitals = {
            "heart_rate": random.randint(55, 160),
            "spo2": random.randint(82, 100),
            "temperature": round(random.uniform(35.5, 40), 1),
            "bp_systolic": random.randint(95, 180)
        }
        res = analyze_vitals(vitals)
        insert_data(vitals, res["severity"], res["reason"])


data = fetch_data()

if data:
    df = pd.DataFrame(data, columns=[
        "id","heart_rate","spo2","temperature",
        "bp_systolic","severity","reason","timestamp"
    ])

    st.metric("Total Records", len(df))

    col1, col2 = st.columns(2)

    with col1:
        st.line_chart(df["heart_rate"])

    with col2:
        st.line_chart(df["spo2"])

    st.dataframe(df)

else:
    st.write("No data available.")
    if st.button("Generate sample records"):
        generate_dummy(10)
        # Streamlit reruns automatically on button press; data will be
        # refreshed in the next run below.