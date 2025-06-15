import streamlit as st

# Page setup
st.set_page_config(page_title="PPH Risk Detection App 💗", page_icon="💓", layout="centered")

# Background style: pink with heart
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffe6f0;
        background-image: url("https://cdn.pixabay.com/photo/2017/01/31/14/32/heart-2029949_1280.png");
        background-repeat: repeat;
        background-size: 80px;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h4 {
        color: #8B0000;
    }
    .css-1v0mbdj p {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='text-align: center;'>💗 PPH Risk Detection App</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Helping rural nurses and pregnant women assess risk in simple steps</h4>", unsafe_allow_html=True)

# Form
with st.form("pph_form"):
    st.write("### Enter Clinical Values (leave blank if not known):")

    bleeding = st.text_input("Estimated Blood Loss (in mL)", help="Normal: <500 mL (normal delivery), <1000 mL (C-section)")
    systolic_bp = st.text_input("Systolic Blood Pressure (mmHg)", help="Normal: 90–120 mmHg")
    diastolic_bp = st.text_input("Diastolic Blood Pressure (mmHg)", help="Normal: 60–80 mmHg")
    heart_rate = st.text_input("Heart Rate (bpm)", help="Normal: 60–100 bpm")
    spo2 = st.text_input("SpO₂ - Oxygen Saturation (%)", help="Normal: 95–100%. Below 92% is low.")
    hemoglobin = st.text_input("Hemoglobin Level (g/dL)", help="Normal: 11–13 g/dL during pregnancy")
    age = st.text_input("Mother's Age (years)", help="Safe age: 18–35 years")
    pod = st.text_input("POD - Post Delivery Day", help="Higher bleeding risk within 3 days after delivery")

    submitted = st.form_submit_button("💖 Check PPH Risk")

def calculate_risk(params):
    risk_score = 0
    notes = []

    if params['bleeding'] and float(params['bleeding']) > 1000:
        risk_score += 2
        notes.append("🔴 Excessive blood loss.")

    if params['systolic'] and float(params['systolic']) < 90:
        risk_score += 1
        notes.append("⚠️ Low systolic BP.")

    if params['diastolic'] and float(params['diastolic']) < 60:
        risk_score += 1
        notes.append("⚠️ Low diastolic BP.")

    if params['heart_rate'] and float(params['heart_rate']) > 100:
        risk_score += 1
        notes.append("⚠️ High heart rate.")

    if params['spo2'] and float(params['spo2']) < 92:
        risk_score += 1
        notes.append("⚠️ Low SpO₂.")

    if params['hemoglobin'] and float(params['hemoglobin']) < 10:
        risk_score += 1
        notes.append("⚠️ Low hemoglobin.")

    if params['age']:
        age_val = float(params['age'])
        if age_val < 18 or age_val > 35:
            risk_score += 1
            notes.append("⚠️ Risk due to age.")

    if params['pod'] and int(params['pod']) <= 3:
        risk_score += 1
        notes.append("⚠️ Early postpartum days.")

    if risk_score >= 4:
        return "🔴 HIGH RISK: Please visit hospital urgently.", notes
    elif risk_score == 3:
        return "🟠 MODERATE RISK: Monitor closely and consult a doctor.", notes
    else:
        return "🟢 LOW RISK: No immediate danger, keep observing.", notes

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
    result, reasons = calculate_risk(inputs)
    st.subheader(result)
    if reasons:
        for r in reasons:
            st.markdown(r)
