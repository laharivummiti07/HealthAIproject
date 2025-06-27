import os
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.granite_api import query_granite

# Set up the page
st.set_page_config(page_title="HealthAI", layout="centered")
st.title("🧠 HealthAI - Intelligent Healthcare Assistant")

# Sidebar navigation
choice = st.sidebar.radio("Choose a feature:", [
    "Patient Chat",
    "Disease Prediction",
    "Treatment Plans",
    "Health Analytics"
])

# ------------------------ Patient Chat ------------------------
def display_patient_chat():
    st.header("🗣️ Patient Chat")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("Ask your health-related question:")
    if user_input:
        response = query_granite(f"Provide a helpful, medically accurate answer: {user_input}")
        st.session_state.chat_history.append({"user": user_input, "ai": response})
        st.json({"response": response})
    
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**AI:** {chat['ai']}")

# --------------------- Disease Prediction ---------------------
def display_disease_prediction():
    st.header("🧬 Disease Prediction")
    symptoms = st.text_area("Describe your symptoms:")
    if st.button("Predict Disease"):
        response = query_granite(
            f"Given the following symptoms: {symptoms}, suggest possible conditions with likelihood and next steps."
        )
        st.json({"prediction": response})

# -------------------- Treatment Plan Generator --------------------
def display_treatment_plans():
    st.header("💊 Treatment Plan Generator")
    condition = st.text_input("Enter diagnosed condition:")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    if st.button("Generate Plan"):
        prompt = f"Create a treatment plan for a {age}-year-old {gender} patient diagnosed with {condition}. Include medications, lifestyle changes, and follow-up advice."
        response = response = query_granite(prompt)
        st.json({"plan": response})

# -------------------- Health Analytics --------------------
def display_health_analytics():
    st.header("📈 Health Analytics")
    
    try:
        data = pd.read_json("data/patient_metrics.json")
        metric = st.selectbox("Choose a metric", ["heart_rate", "blood_pressure", "glucose"])
        fig = px.line(data, x="dates", y=metric, title=f"{metric.title()} Over Time")
        st.plotly_chart(fig)

        insight_prompt = f"Analyze the trend for {metric} values: {data[metric].tolist()}. Give health insights and improvement tips."
        insights = query_granite(insight_prompt)
        st.json({"insights": insights})
    except Exception as e:
        st.error(f"Error loading health data: {e}")

# ---------------------- Main Routing ----------------------
if choice == "Patient Chat":
    display_patient_chat()
elif choice == "Disease Prediction":
    display_disease_prediction()
elif choice == "Treatment Plans":
    display_treatment_plans()
elif choice == "Health Analytics":
    display_health_analytics()
