import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Machine Failure Prediction", layout="wide")

st.title("⚙️ Machine Failure Prediction App")
st.write("Upload your machine parameters to predict whether failure will occur.")

# ------------------------------------------------------
# SAFE MODEL LOADING (fixed paths + error handling)
# ------------------------------------------------------
@st.cache_resource
def load_model(path):
    if not os.path.exists(path):
        st.error(f"Model file not found: {path}")
        st.stop()
    with open(path, "rb") as f:
        return pickle.load(f)

# Relative paths (fixed)
model_paths = {
    "Logistic Regression": "final_model_pipeline_lr.pkl",
    "LightGBM": "final_model_pipeline_lgb.pkl",
    "Random Forest": "final_model_pipeline_rfr.pkl",
    "XGBoost": "final_model_pipeline_xgb.pkl",
}

loaded_models = {}
for name, path in model_paths.items():
    try:
        loaded_models[name] = load_model(path)
    except Exception as e:
        st.error(f" Failed to load {name}: {e}")

# ------------------------------------------------------
# USER INPUT PANEL
# ------------------------------------------------------
st.sidebar.header("Input Features")

air_temp = st.sidebar.number_input("Air Temperature (°C)", min_value=250, max_value=400, value=300)
process_temp = st.sidebar.number_input("Process Temperature (°C)", min_value=250, max_value=400, value=305)
rot_speed = st.sidebar.number_input("Rotational Speed (rpm)", min_value=500, max_value=5000, value=1800)
torque = st.sidebar.number_input("Torque (Nm)", min_value=0, max_value=100, value=40)
tool_wear = st.sidebar.number_input("Tool Wear (min)", min_value=0, max_value=300, value=150)

model_choice = st.sidebar.selectbox("Choose Prediction Model", list(loaded_models.keys()))

# ------------------------------------------------------
# INPUT DATAFRAME (fixed Kelvin conversion)
# ------------------------------------------------------
input_data = pd.DataFrame({
    "Air temperature [K]": [air_temp + 273.15],
    "Process temperature [K]": [process_temp + 273.15],
    "Rotational speed [rpm]": [rot_speed],
    "Torque [Nm]": [torque],
    "Tool wear [min]": [tool_wear],
})

# ------------------------------------------------------
# PREDICT
# ------------------------------------------------------
if st.button("Predict Failure"):
    model = loaded_models[model_choice]

    try:
        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

        st.subheader(" Prediction Result")
        if prediction == 1:
            st.error(f"Machine is likely to FAIL (Probability: {prob:.2f})")
        else:
            st.success(f"Machine is SAFE (Failure probability: {prob:.2f})")

        st.write("---")
        st.write("### Input Summary")
        st.dataframe(input_data)

    except Exception as e:
        st.error(f" Prediction Error: {e}")
