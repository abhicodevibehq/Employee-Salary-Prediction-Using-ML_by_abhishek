import streamlit as st
import joblib
import pandas as pd
import os

# --- Custom CSS for dark mode and layout ---
st.markdown('''
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    body, .stApp { background: #111214 !important; }
    .main-card {
        background: #18191c;
        border-radius: 20px;
        box-shadow: 0 4px 32px 0 #0003, 0 0 0 2px #2546ff33;
        padding: 2.5vw 3vw 2vw 3vw;
        margin: 5vw auto 0 auto;
        max-width: 700px;
        width: 95vw;
        border: 1.5px solid #23243a;
    }
    .header-card {
        background: #18191c;
        border-radius: 20px 20px 0 0;
        padding: 2vw 3vw 1vw 3vw;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1.5px solid #23243a;
        margin-bottom: 0;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 3vw;
    }
    .app-title {
        color: #fff;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0;
    }
    .app-title span {
        color: #5fa8f6;
    }
    .header-icons {
        display: flex;
        gap: 3vw;
        font-size: 1.5rem;
    }
    .header-icons a {
        color: #bfc6d1;
        transition: color 0.2s;
        text-decoration: none;
    }
    .header-icons a:hover {
        color: #5fa8f6;
    }
    .form-card {
        background: #18191c;
        border-radius: 16px;
        padding: 5vw 3vw 3vw 3vw;
        margin-bottom: 4vw;
        border: 1.5px solid #23243a;
        width: 100%;
        box-sizing: border-box;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div>div {
        background: #23243a !important;
        color: #fff !important;
        border-radius: 10px !important;
        border: 1.5px solid #23243a !important;
        font-weight: 500;
        font-size: 1rem;
    }
    .stTextInput>label, .stNumberInput>label, .stSelectbox>label {
        color: #bfc6d1 !important;
        font-weight: 600;
        margin-bottom: 2px;
        font-size: 1rem;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.7em 0;
        margin-top: 10px;
        margin-bottom: 0;
        width: 100%;
        background: linear-gradient(90deg,#2546ff 60%,#5fa8f6 100%);
        color: #fff;
        border: none;
        box-shadow: 0 2px 8px 0 #2546ff44;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg,#5fa8f6 60%,#2546ff 100%);
        color: #fff;
    }
    .reset-btn {
        background: #23243a !important;
        color: #bfc6d1 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        margin-top: 10px;
        width: 100%;
    }
    .footer {
        color: #bfc6d1;
        text-align: center;
        font-size: 1rem;
        margin-top: 32px;
        margin-bottom: 8px;
    }
    .footer a { color: #5fa8f6; text-decoration: none; font-weight: 700; }
    .footer a:hover { text-decoration: underline; }
    .predicted-salary-btn {
        width: 100%;
        background: #23243a !important;
        color: #bfc6d1 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        margin-top: 10px;
        padding: 0.7em 0;
        box-shadow: 0 0 12px 0 #2546ff44;
        cursor: not-allowed;
        display: block;
        text-align: center;
    }
    .reset-btn-custom {
        width: 100%;
        background: transparent !important;
        color: #ff4b4b !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: 1.5px solid #ff4b4b !important;
        margin-top: 10px;
        padding: 0.7em 0;
        box-shadow: none;
        cursor: pointer;
        display: block;
        text-align: center;
        transition: background 0.2s, color 0.2s;
    }
    .reset-btn-custom:hover {
        background: #ff4b4b22 !important;
        color: #fff !important;
    }
    .desc-accuracy-box {
      background: #18191c;
      border-radius: 14px;
      margin: 2vw 0 2vw 0;
      padding: 4vw 4vw 3vw 4vw;
      box-shadow: 0 2px 12px 0 #2546ff22;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      width: 100%;
      box-sizing: border-box;
    }
    .desc-text {
      color: #bfc6d1;
      font-size: 1.08rem;
      font-weight: 500;
      letter-spacing: 0.1px;
      line-height: 1.5;
    }
    .accuracy-pill {
      display: flex;
      align-items: center;
      gap: 10px;
      background: linear-gradient(90deg,#2546ff 0%,#5fa8f6 100%);
      color: #fff;
      font-weight: 800;
      font-size: 1.08rem;
      border-radius: 999px;
      padding: 10px 26px;
      box-shadow: 0 0 16px 0 #2546ff66;
      letter-spacing: 0.5px;
      margin-left: auto;
      border: none;
      min-width: 180px;
      justify-content: center;
    }
    .accuracy-icon {
      font-size: 1.25em;
      margin-right: 2px;
    }
    /* Responsive styles */
    @media (max-width: 900px) {
      .main-card, .form-card, .desc-accuracy-box { max-width: 98vw; padding-left: 2vw; padding-right: 2vw; }
      .header-card { flex-direction: column; gap: 1vw; padding: 2vw 2vw 1vw 2vw; }
      .header-icons { gap: 2vw; }
    }
    @media (max-width: 600px) {
      .main-card, .form-card, .desc-accuracy-box { max-width: 100vw; padding-left: 1vw; padding-right: 1vw; }
      .desc-accuracy-box { flex-direction: column; align-items: flex-start; gap: 10px; }
      .accuracy-pill { margin-left: 0; width: 100%; justify-content: flex-start; }
      .header-card { flex-direction: column; gap: 2vw; padding: 2vw 1vw 1vw 1vw; }
      .header-left { gap: 2vw; }
      .header-icons { gap: 2vw; }
      .app-title { font-size: 1.4rem; }
      .desc-text { font-size: 0.98rem; }
      .accuracy-pill { font-size: 0.98rem; padding: 8px 10px; }
      .form-card { padding: 4vw 2vw 2vw 2vw; }
    }
    </style>
''', unsafe_allow_html=True)

# --- Header ---
header_cols = st.columns([0.1, 0.6, 0.3])
with header_cols[0]:
    st.image('static/app-logo.png', width=54)
with header_cols[1]:
    st.markdown('<span class="app-title"><span>Salary</span> Scope</span>', unsafe_allow_html=True)
with header_cols[2]:
    st.markdown('''
    <div class="header-icons">
      <a href="https://github.com/SpicychieF05" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
      <a href="https://www.linkedin.com/in/chirantan-mallick" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
      <a href="https://x.com/Chirantan2965" target="_blank" title="Twitter"><i class="fab fa-twitter"></i></a>
      <a href="https://discord.gg/mc2jRBuV" target="_blank" title="Discord"><i class="fab fa-discord"></i></a>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('''
<style>
.header-flex {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 900px;
  margin: 0 auto 0 auto;
  padding: 0 2vw 0 2vw;
  min-height: 80px;
}
.header-left-flex {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 18px;
}
.header-icons {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 18px;
  font-size: 1.35rem;
  margin-top: 2px;
}
.header-icons a {
  color: #bfc6d1;
  transition: color 0.2s;
  text-decoration: none;
  display: flex;
  align-items: center;
}
.header-icons a:hover {
  color: #5fa8f6;
}
@media (max-width: 700px) {
  .header-flex {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 0 1vw 0 1vw;
  }
  .header-icons {
    gap: 18px;
    font-size: 1.5rem;
  }
  .app-title {
    font-size: 1.3rem;
  }
}
</style>
''', unsafe_allow_html=True)

# --- Description and Accuracy ---
st.markdown('''
<div class="desc-accuracy-box">
  <div class="desc-text">   
    Salary Scope predicts your expected salary based on your profile and job details. Enter your information below to get an instant, data-driven estimate.
  </div>
  <div class="accuracy-pill">
    <span class="accuracy-icon">✔️</span>
    <span class="accuracy-text"><b>Accuracy: 89% (R² = 0.89)</b></span>
  </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<style>
.desc-accuracy-box {
  background: #18191c;
  border-radius: 14px;
  margin: 2vw 0 2vw 0;
  padding: 4vw 4vw 3vw 4vw;
  box-shadow: 0 2px 12px 0 #2546ff22;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 3vw;
  width: 100%;
  box-sizing: border-box;
}
.desc-text {
  color: #bfc6d1;
  font-size: 1.15rem;
  font-weight: 500;
  letter-spacing: 0.1px;
  line-height: 1.5;
  flex: 1 1 0;
  display: flex;
  align-items: center;
}
.accuracy-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(90deg,#2546ff 0%,#5fa8f6 100%);
  color: #fff;
  font-weight: 800;
  font-size: 1.08rem;
  border-radius: 999px;
  padding: 18px 36px;
  box-shadow: 0 0 16px 0 #2546ff66;
  letter-spacing: 0.5px;
  margin-left: 2vw;
  border: none;
  min-width: 180px;
  justify-content: center;
  text-align: left;
}
.accuracy-icon {
  font-size: 1.25em;
  margin-right: 2px;
}
@media (max-width: 900px) {
  .desc-accuracy-box { gap: 2vw; padding: 4vw 2vw 3vw 2vw; }
  .accuracy-pill { padding: 14px 18px; font-size: 1rem; }
}
@media (max-width: 600px) {
  .desc-accuracy-box {
    flex-direction: column;
    align-items: stretch;
    gap: 18px;
    padding: 4vw 2vw 3vw 2vw;
  }
  .desc-text {
    font-size: 1rem;
    justify-content: flex-start;
    align-items: flex-start;
  }
  .accuracy-pill {
    margin-left: 0;
    width: 100%;
    justify-content: flex-start;
    padding: 12px 10px;
    font-size: 0.98rem;
  }
}
.form-card {
  background: #18191c;
  border-radius: 16px;
  padding: 28px 24px 22px 24px;
  margin-top: 8px; /* reduced top margin */
  margin-bottom: 32px;
  border: 1.5px solid #23243a;
}
</style>
''', unsafe_allow_html=True)

# --- Form Card ---
st.markdown('<div class="form-card">', unsafe_allow_html=True)

# Dropdown options
job_titles = sorted([
    'Actuary', 'Agile Coach', 'AI Engineer', 'Assistant Engineer (AE)', 'Assistant Section Officer', 'Auditor', 'Automation Tester', 'Backend Developer', 'Bank Clerk', 'Bank Probationary Officer (PO)', 'Bank Specialist Officer (SO)', 'Big Data Engineer', 'Block Development Officer (BDO)', 'Blockchain Developer', 'Business Analyst', 'Business Intelligence Developer', 'Chartered Accountant (CA)', 'Chief Technology Officer (CTO)', 'Cloud Architect', 'Cloud Engineer', 'Cloud Security Engineer', 'Company Secretary (CS)', 'Content Strategist', 'Cost Accountant (CMA)', 'CRM Specialist (Salesforce)', 'Credit Analyst', 'Customs Officer', 'Cybersecurity Analyst', 'Data Analyst', 'Data Engineer', 'Data Scientist', 'Database Administrator (DBA)', 'Deep Learning Engineer', 'DevOps Engineer', 'Digital Marketing Analyst', 'District Magistrate', 'Embedded Systems Engineer', 'ERP Consultant (SAP/Oracle)', 'Excise Officer', 'Financial Analyst', 'Financial Planner', 'Frontend Developer', 'Full Stack Developer', 'Game Developer', 'Graphic Designer', 'IAS Officer', 'IFS Officer', 'Income Tax Inspector', 'Indian Railways Officer (RRB Group A/B)', 'Information Security Officer', 'Insurance Advisor (GIC/NIC)', 'IoT Engineer', 'IPS Officer', 'IRS Officer', 'IT Consultant', 'IT Project Manager', 'IT Support Specialist', 'Junior Engineer (JE)', 'LDC (Lower Division Clerk)', 'LIC AAO', 'LIC ADO', 'Loan Officer', 'Machine Learning Engineer', 'Mobile App Developer', 'Mutual Fund Advisor', 'NABARD Grade A/B Officer', 'NLP Engineer', 'Network Administrator', 'Network Engineer', 'Portfolio Manager', 'Power BI Developer', 'Product Manager', 'PSU Engineer (ONGC, NTPC, BHEL)', 'QA/Test Engineer', 'Railway Protection Force (RPF) Officer', 'RBI Assistant', 'RBI Grade B Officer', 'Research Officer (CSIR/ICAR)', 'Risk Analyst', 'Scrum Master', 'SEBI Grade A Officer', 'SEO Specialist', 'Social Media Manager', 'Software Architect', 'Software Developer', 'SSC CGL Officer', 'State PCS Officer', 'Stock Broker', 'System Administrator', 'Tax Consultant', 'Technical Support Engineer', 'Tehsildar', 'Treasury Manager', 'UI/UX Designer', 'UDC (Upper Division Clerk)', 'Wealth Manager', 'Web Designer'
])
locations = ['Rural', 'Suburban', 'Urban']
nationalities = sorted(['American', 'Australian', 'Brazilian', 'British', 'Canadian', 'Chinese', 'French', 'German', 'Indian', 'Japanese', 'Russian', 'South African'])

with st.form("salary_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input("Age", placeholder="e.g., 35")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
    with col3:
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"], index=1)
    col4, col5 = st.columns(2)
    with col4:
        job_title = st.selectbox("Job Title", job_titles, index=job_titles.index("Software Developer") if "Software Developer" in job_titles else 0)
    with col5:
        years_of_experience = st.text_input("Years of Experience", placeholder="e.g., 5")
    col6, col7, col8 = st.columns(3)
    with col6:
        education = st.selectbox("Highest Education", ["PhD", "Masters", "Bachelors", "12th", "10th"], index=0)
    with col7:
        education_num = st.text_input("Education (Numeric)", placeholder="e.g., 15 for Bachelors")
    with col8:
        hours_per_week = st.text_input("Hours per Week", placeholder="e.g., 45")
    col9, col10, col11 = st.columns(3)
    with col9:
        city = st.text_input("City", placeholder="e.g., Mumbai")
    with col10:
        location = st.selectbox("Location Type", locations, index=2)
    with col11:
        nationality = st.selectbox("Nationality", nationalities, index=nationalities.index("Indian") if "Indian" in nationalities else 0)
    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB, colC = st.columns([1,1,1])
    with colA:
        predict_btn = st.form_submit_button("🧑‍💼 Predict Salary")
    with colB:
        st.markdown('''
    <button class="custom-btn predicted-salary-btn" disabled>
      <span class="predicted-salary-hint">Check your Salary Below</span>
    </button>
    ''', unsafe_allow_html=True)
    with colC:
        reset_btn = st.form_submit_button("Reset")

st.markdown('</div>', unsafe_allow_html=True)  # Close form-card

# --- Footer ---
st.markdown('''
<div class="footer">
  &copy; 2025 Salary Scope. All rights reserved.<br>
  Developed by <a href="https://linktr.ee/chirantan_mallick" target="_blank">Chirantan Mallick</a>
</div>
</div>
''', unsafe_allow_html=True)

# --- Model and Prediction Logic ---
import joblib
model = joblib.load('model.joblib')
label_encoder = joblib.load('label_encoder.joblib')

def is_valid(val):
    return val not in (None, "", "Select")

predicted_salary = None
prediction_error = None
if 'predict_btn' in locals() and predict_btn:
    if not all([
        is_valid(age), is_valid(gender), is_valid(marital_status),
        is_valid(job_title), is_valid(years_of_experience), is_valid(education),
        is_valid(education_num), is_valid(hours_per_week), is_valid(city),
        is_valid(location), is_valid(nationality)
    ]):
        st.error("Please fill in all fields.")
    else:
        try:
            input_df = pd.DataFrame([{
                "gender": gender,
                "education": education,
                "job_title": job_title,
                "job_location": location,
                "city": city,
                "nationality": nationality,
                "marital_status": marital_status,
                "age": int(age),
                "years_of_experience": int(years_of_experience),
                "education_num": int(education_num),
                "hours_per_week": int(hours_per_week)
            }])
            prediction = model.predict(input_df)
            predicted_salary = f"Predicted Salary: ₹{prediction[0]:,.0f} lakhs"
        except Exception as e:
            prediction_error = f"Error in prediction: {e}"

# --- Neon Box CSS ---
st.markdown('''
<style>
.neon-box {
    position: relative;
    background: #18191c;
    border-radius: 18px;
    margin: 32px auto 0 auto;
    padding: 32px 24px 24px 24px;
    max-width: 500px;
    text-align: center;
    color: #e0e6f7;
    font-size: 1.5rem;
    font-weight: 700;
    box-shadow: 0 0 32px 0 #2546ff44;
    overflow: hidden;
}
.neon-rotate {
    position: absolute;
    top: -4px; left: -4px; right: -4px; bottom: -4px;
    border-radius: 22px;
    pointer-events: none;
    z-index: 0;
}
.neon-rotate::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 22px;
    border: 4px solid transparent;
    background: conic-gradient(
        #2546ff 0deg, #5fa8f6 90deg, #2546ff 180deg, #5fa8f6 270deg, #2546ff 360deg
    );
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    animation: neon-rotate 2.5s linear infinite;
}
@keyframes neon-rotate {
    100% { transform: rotate(360deg); }
}
</style>
''', unsafe_allow_html=True)

# --- Show Neon Box if Prediction ---
if predicted_salary:
    st.markdown('''
    <div class="neon-box">
      <div class="neon-rotate"></div>
      <span style="position:relative;z-index:1;">{}</span>
      <div style="font-size:1rem;font-weight:400;color:#5fa8f6;margin-top:8px;">Authenticity: 89% (R² = 0.89)</div>
    </div>
    '''.format(predicted_salary), unsafe_allow_html=True)
if prediction_error:
    st.error(prediction_error)

st.markdown('''
    <style>
    .custom-btn {
        width: 100%;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-top: 10px;
        padding: 0.7em 0;
        display: block;
        text-align: center;
        box-shadow: 0 0 12px 0 #2546ff44;
        transition: background 0.2s, color 0.2s;
        border: 1.5px solid #23243a !important;
        background: #18191c !important;
    }
    .predict-btn {
        color: #fff !important;
        border: 1.5px solid #5fa8f6 !important;
    }
    .predict-btn:hover {
        background: #2546ff44 !important;
        color: #5fa8f6 !important;
    }
    .predicted-salary-btn {
        color: #bfc6d1 !important;
        background: #23243a !important;
        border: none !important;
        cursor: not-allowed;
    }
    .predicted-salary-hint {
        display: block;
        font-size: 0.85em;
        color: #5fa8f6;
        text-shadow: 0 0 8px #2546ff, 0 0 2px #5fa8f6;
        font-weight: 500;
        margin-bottom: 2px;
        letter-spacing: 0.5px;
    }
    .predicted-salary-main {
        font-size: 1.18em;
        font-weight: 700;
        color: #bfc6d1;
    }
    .reset-btn-custom {
        color: #ff4b4b !important;
        border: 1.5px solid #ff4b4b !important;
        background: transparent !important;
    }
    .reset-btn-custom:hover {
        background: #ff4b4b22 !important;
        color: #fff !important;
    }
    [data-testid="stFormSubmitButton"] button {
        width: 100% !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-top: 10px !important;
        padding: 0.7em 0 !important;
        background: linear-gradient(90deg,#2546ff 60%,#5fa8f6 100%) !important;
        color: #fff !important;
        border: none !important;
        box-shadow: 0 2px 8px 0 #2546ff44 !important;
        transition: background 0.2s !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(90deg,#5fa8f6 60%,#2546ff 100%) !important;
        color: #fff !important;
    }
    </style>
''', unsafe_allow_html=True)
