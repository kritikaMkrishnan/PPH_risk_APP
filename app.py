import streamlit as st
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="PPH Risk Detection App 💗", page_icon="💓", layout="centered")

# Custom font and color styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #ffe4e1;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cpath fill='%23ff9999' d='M50,0 Q60,20 80,10 Q90,30 100,20 V100 H0 V20 Q10,30 20,10 Q40,20 50,0 Z'/%3E%3C/svg%3E");
        background-size: 100px 100px;
    }

    h1 {
        color: #000000; /* Black for high contrast */
        font-weight: 700;
    }

    h4 {
        color: #333333; /* Dark gray for a softer subtitle */
        font-weight: 400;
    }

    .css-1v0mbdj p {
        font-size: 16px;
        color: #333333; /* Dark gray for body text */
    }
    
    .stButton>button {
        background-color: #ff6699;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown("<h1 style='text-align: center;'>💗 PPH Risk Detection App</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Helping rural nurses and pregnant women assess risk easily</h4>", unsafe_allow_html=True)

# Introduction
with st.expander("📘 What is PPH? (Postpartum Hemorrhage)"):
    st.markdown("""
    **Postpartum Hemorrhage (PPH)** is excessive bleeding after childbirth. It is one of the **leading causes of maternal deaths worldwide**, especially in low-resource settings.

    - 🔴 **PPH can occur within 24 hours or up to several days after delivery.**
    - 📊 Globally, PPH contributes to **more than 25% of maternal deaths**.
    - 🚑 Early detection and response can **save lives**.

    This tool helps healthcare staff and pregnant women to identify risk signs early using simple inputs.
    """)

# Form
with st.form("pph_form"):
    st.write("### Enter Patient & Clinical Details")

    name = st.text_input("Patient Name")
    reg_no = st.text_input("Registration Number (Optional)")
    bleeding = st.text_input("Estimated Blood Loss (mL)", help="Normal: <500 mL (vaginal), <1000 mL (C-section)")
    systolic_bp = st.text_input("Systolic Blood Pressure (mmHg)", help="Normal: 90–120 mmHg")
    diastolic_bp = st.text_input("Diastolic Blood Pressure (mmHg)", help="Normal: 60–80 mmHg")
    heart_rate = st.text_input("Heart Rate (bpm)", help="Normal: 60–100 bpm")
    spo2 = st.text_input("SpO₂ (%)", help="Normal: 95–100%. Below 92% is low.")
    hemoglobin = st.text_input("Hemoglobin Level (g/dL)", help="Normal: 11–13 g/dL in pregnancy")
    age = st.text_input("Mother's Age (years)", help="Safe age: 18–35 years")
    pod = st.text_input("POD - Post Delivery Day", help="Higher bleeding risk within 3 days")

    submitted = st.form_submit_button("💖 Check PPH Risk")

    if submitted:
        inputs = {
            'bleeding': bleeding.strip() or None,
            'systolic': systolic_bp.strip() or None,
            'diastolic': diastolic_bp.strip() or None,
            'heart_rate': heart_rate.strip() or None,
            'spo2': spo2.strip() or None,
            'hemoglobin': hemoglobin.strip() or None,
            'age': age.strip() or None,
            'pod': pod.strip() or None
        }

        def calculate_risk(params):
            risk_score = 0
            notes = []

            if params['bleeding'] and float(params['bleeding']) > 1000:
                risk_score += 2
                notes.append("🔴 Excessive blood loss")

            if params['systolic'] and float(params['systolic']) < 90:
                risk_score += 1
                notes.append("⚠️ Low systolic BP")

            if params['diastolic'] and float(params['diastolic']) < 60:
                risk_score += 1
                notes.append("⚠️ Low diastolic BP")

            if params['heart_rate'] and float(params['heart_rate']) > 100:
                risk_score += 1
                notes.append("⚠️ High heart rate")

            if params['spo2'] and float(params['spo2']) < 92:
                risk_score += 1
                notes.append("⚠️ Low SpO₂")

            if params['hemoglobin'] and float(params['hemoglobin']) < 10:
                risk_score += 1
                notes.append("⚠️ Low hemoglobin")

            if params['age']:
                age_val = float(params['age'])
                if age_val < 18 or age_val > 35:
                    risk_score += 1
                    notes.append("⚠️ Risk due to age")

            if params['pod'] and int(params['pod']) <= 3:
                risk_score += 1
                notes.append("⚠️ Early postpartum days")

            if risk_score >= 4:
                return "🔴 HIGH RISK: Please visit hospital urgently.", notes
            elif risk_score == 3:
                return "🟠 MODERATE RISK: Monitor closely and consult a doctor.", notes
            else:
                return "🟢 LOW RISK: No immediate danger, keep observing.", notes

        result, reasons = calculate_risk(inputs)

        st.subheader("💡 Result")
        st.markdown(f"**{result}**")
        if reasons:
            st.markdown("#### Reasoning:")
            for r in reasons:
                st.markdown(r)

        # Collect data for download
        data = {
            "Name": [name],
            "Reg No": [reg_no],
            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "Blood Loss (mL)": [bleeding],
            "Systolic BP": [systolic_bp],
            "Diastolic BP": [diastolic_bp],
            "Heart Rate": [heart_rate],
            "SpO2": [spo2],
            "Hemoglobin": [hemoglobin],
            "Age": [age],
            "POD": [pod],
            "Risk Level": [result]
        }

        df = pd.DataFrame(data)

        # Download CSV
        st.markdown("### 📥 Download Report")
        st.download_button(
            label="Download Report as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"{name}_PPH_Report.csv",
            mime='text/csv'
        )




