import streamlit as st
import pandas as pd
import requests
import joblib
import io

st.title("Machine Failure Predictor")

st.write("Upload your CSV below:")

uploaded_file = st.file_uploader("Select CSV", type=["csv"])

# --------------------------
# DELAYED MODEL LOADING
# --------------------------
model_urls = {
    "model_1": "https://github.com/DURVA-GARGGG/machine_failure-app/releases/download/v1/model1.pkl",
    "model_2": "https://github.com/DURVA-GARGGG/machine_failure-app/releases/download/v1/model2.pkl",
    "model_3": "https://github.com/DURVA-GARGGG/machine_failure-app/releases/download/v1/model3.pkl",
}

loaded_models = {}  # empty at start


def load_models_on_demand():
    # Only load if not already loaded
    if loaded_models:
        return loaded_models

    progress = st.progress(0)
    status = st.empty()

    total = len(model_urls)
    for i, (name, url) in enumerate(model_urls.items(), start=1):
        status.write(f"Downloading **{name}** ...")

        response = requests.get(url)
        response.raise_for_status()

        file_like = io.BytesIO(response.content)
        loaded_models[name] = joblib.load(file_like)

        progress.progress(i / total)

    status.success("Models loaded successfully!")
    return loaded_models


# --------------------------
#     MAIN APP UI
# --------------------------

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Data:")
    st.dataframe(df)

    if st.button("🔄 Load Models"):
        models = load_models_on_demand()

    if st.button("🚀 Predict Failure"):
        if not loaded_models:
            st.error("Please load models first using the button above.")
        else:
            model = loaded_models["model_1"]  # your primary model
            preds = model.predict(df)
            st.write("### Prediction Output:")
            st.write(preds)
