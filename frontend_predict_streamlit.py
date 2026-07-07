import streamlit as st
import requests

# FastAPI endpoint (update if needed)
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Insurance Premium Category Predictor", layout="centered")
st.title("Insurance Premium Category Predictor")
st.caption("Frontend for the FastAPI /predict endpoint")

st.markdown("---")

with st.form("predict_form"):
    st.subheader("Enter your details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.1, value=65.0, step=0.1)
        height = st.number_input("Height (m)", min_value=0.1, max_value=2.5, value=1.7, step=0.01)

    with col2:
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, step=0.1)
        smoker = st.selectbox("Are you a smoker?", options=[True, False])
        city = st.text_input("City", value="Mumbai")

    occupation = st.selectbox(
        "Occupation",
        options=[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        index=6,
    )

    submit = st.form_submit_button("Predict Premium Category")

if submit:
    payload = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "smoker": bool(smoker),
        "city": city,
        "occupation": occupation,
    }

    try:
        res = requests.post(API_URL, json=payload, timeout=15)
        # surface backend error payload if any
        res.raise_for_status()
        data = res.json()

        predicted = data.get("predicted_category")
        if predicted is None:
            st.error(f"Unexpected response format: {data}")
        else:
            st.success(f"Predicted Insurance Premium Category: {predicted}")
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        st.info(f"Check that FastAPI is running and API_URL is correct: {API_URL}")

