import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

st.set_page_config(page_title="Brain Tumor Classifier", layout="wide")

st.title("🧠 Brain Tumor Classifier")

# -------------------------------
# 1️⃣ LOAD YOUR DATASET SAFELY
# -------------------------------
FILE_PATH = "newcsv.csv"   # FINAL FIXED NAME

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(FILE_PATH)
        return df, None
    except Exception as e:
        return None, str(e)

df, error = load_data()

if error:
    st.error(f"❌ Could not load '{FILE_PATH}'. Make sure the file exists.\n\nError: {error}")
    st.stop()

st.success("✅ Dataset loaded successfully!")

st.write("### Preview of your data")
st.dataframe(df.head())

# ---------------------------------
# 2️⃣ PREPARE FEATURES + LABEL
# ---------------------------------
X = df.drop(columns=["Tumor"])
y = df["Tumor"]

# ---------------------------------
# 3️⃣ TRAIN-TEST SPLIT
# ---------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------
# 4️⃣ BUILD ALL 4 MODELS
# ---------------------------------
models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression())
    ]),

    "LightGBM": LGBMClassifier(),

    "Random Forest": RandomForestClassifier(),

    "XGBoost": XGBClassifier(
        eval_metric="logloss",
        use_label_encoder=False
    )
}

# ---------------------------------
# 5️⃣ FIT MODELS SAFELY
# ---------------------------------
status = {}

for name, model in models.items():
    try:
        model.fit(X_train, y_train)
        status[name] = "fitted"
    except Exception as e:
        status[name] = f"ERROR: {e}"

# ---------------------------------
# 6️⃣ USER INPUT — SIMPLE TEST CASE
# ---------------------------------
st.write("### 🔍 Enter Tumor Features for Prediction")

user_input = {}
for col in X.columns:
    user_input[col] = st.number_input(f"{col}", value=float(df[col].mean()))

user_data = pd.DataFrame([user_input])

# ---------------------------------
# 7️⃣ SHOW RESULTS TABLE
# ---------------------------------
st.write("### 📌 Model Predictions")

result_table = []

for name, model in models.items():
    if status[name] != "fitted":
        result_table.append([name, "ERROR", "—", status[name]])
        continue

    try:
        pred = model.predict(user_data)[0]
        prob = model.predict_proba(user_data)[0].max()
        result_table.append([name, pred, f"{prob:.4f}", "OK"])
    except Exception as e:
        result_table.append([name, "ERROR", "—", str(e)])

final_df = pd.DataFrame(
    result_table,
    columns=["Model", "Prediction", "Probability", "Status"]
)

st.dataframe(final_df, use_container_width=True)
