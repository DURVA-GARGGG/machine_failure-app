import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.set_page_config(page_title="Machine Failure Prediction", layout="wide")

st.title("⚙️ Machine Failure Prediction App")
st.write("Upload your machine parameters to predict whether failure will occur.")

# -------------------------------
# Load Models
# -------------------------------
@st.cache_resource
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

model_paths = {
    "Logistic Regression": "models/final_model_pipeline_lr.pkl",
    "LightGBM": "models/final_model_pipeline_lgb.pkl",
    "Random Forest": "models/final_model_pipeline_rfr.pkl",
    "XGBoost": "models/final_model_pipeline_xgb.pkl",
}

loaded_models = {
    name: load_model(path) for name, path in model_paths.items()
}

# -------------------------------
# User Input
# ---------------------------
st.sidebar.header("Input Features")

air_temp = st.sidebar.number_input("Air Temperature (°C)", 250, 400, 300)
process_temp = st.sidebar.number_input("Process Temperature (°C)", 250, 400, 305)
rot_speed = st.sidebar.number_input("Rotational Speed (rpm)", 500, 5000, 1800)
torque = st.sidebar.number_input("Torque (Nm)", 0, 100, 40)
tool_wear = st.sidebar.number_input("Tool Wear (min)", 0, 300, 150)

model_choice = st.sidebar.selectbox(
    "Choose Prediction Model", list(loaded_models.keys())
)

input_data = pd.DataFrame({
    "Air temperature [K]": [air_temp + 273],
    "Process temperature [K]": [process_temp + 273],
    "Rotational speed [rpm]": [rot_speed],
    "Torque [Nm]": [torque],
    "Tool wear [min]": [tool_wear],
})

# -------------------------------
# Predict
# -------------------------------
if st.button("Predict Failure "):
    model = loaded_models[model_choice]
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    st.subheader(" Prediction Result:")
    if prediction == 1:
        st.error(f"Machine is likely to FAIL (probability: {prob:.2f})")
    else:
        st.success(f" Machine is SAFE (probability of failure: {prob:.2f})")

    st.write("---")
    st.write("### 🌡 Input Summary")
    st.write(input_data)
