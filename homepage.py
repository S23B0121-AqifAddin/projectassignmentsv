import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components
import time

#SETUP SETTING
st.markdown(
    """
    <style>
  /* Background image container */
    .title-container {
        position: relative;
        width: fit-content; /* width adjusts to content */
        margin: 0 auto; /* center horizontally */
        border-radius: 12px;
        overflow: hidden; /* ensures rounded corners apply to children */
    }

    /* Background image */
    .title-bg {
        background-image: url("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e");
        background-size: cover;
        background-position: center;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 200px; /* height of the image box */
    }

    /* Transparent black overlay */
    .title-overlay {
        background-color: rgba(0, 0, 0, 0.5); /* Transparent black */
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Title text */
    .title-overlay h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }

    p {
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display title inside transparent black box
st.markdown(
    """
   <div class="title-container">
        <div class="title-bg">
            <div class="title-overlay">
                <h1>💵💷Financial Behaviour among University Students💴💶</h1>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#RealTimeData
# ----------------------------
# Google Form Expander
# ----------------------------
with st.expander("📝 Fill the Google Form", expanded=False):
    FORM_IFRAME = """
    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSc64KYOt8YZMIo559AdmO8p-4uAhPm7rYE9uY8R36KNIm4dhw/viewform?embedded=true"
    width="100%" height="900" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    """
    components.html(FORM_IFRAME, height=920)

# ----------------------------
# Live Responses Expander
# ----------------------------
with st.expander("📊 Live Responses", expanded=False):
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    client = gspread.authorize(creds)

    SHEET_ID = "1vpYf97ioLU7dVFbVCzrb73fALQAnOL9j17C2luNB1To"
    SHEET_NAME = "Form Responses 1"

    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    df = pd.DataFrame(sheet.get_all_records())
    st.dataframe(df)
     # Show dynamic rows × columns info
    st.markdown(f"**Rows:** {df.shape[0]} × **Columns:** {df.shape[1]}")


#PAGE
# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="💵💷Financial Behaviour among University Students💴💶",
    layout="wide" # Set layout here for consistency
)

st.markdown("---")
st.header("📈📉Original Dataset(Without Cleaning)")
#Load Original Dataset
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='latin-1')
df
# Display row × column info
st.markdown(f"<div style='font-size:12px; color:gray; margin:0; padding:0;'>Rows: {df.shape[0]} × Columns: {df.shape[1]}</div>", unsafe_allow_html=True)
st.markdown("---")

#OBJECTIVE AND PROBLEM
# =========================
# 1. Objective
# =========================
st.subheader("Objective")
st.write(
    """
    The objective of this study is to use scientific visualisation techniques to examine university student's
    financial literacy and consumer behaviour in order to find important trends and connections that can help
    with successful financial education and industry activities.
    """
)

# =========================
# 2. Problem Definition
# =========================
st.subheader("Problem Definition")
st.write(
    """
   Low financial knowledge among university students often results in bad consumer behaviour, including overspending,
   building up debt and inappropriate usage of financial services. Scientific visualisation is required to
   help uncover trends and threats within student financial data since traditional data analysis methods have
   limitations in their ability to show complicated behavioural patterns.
    """
)

st.markdown("---")
st.write("""
### Group Overview
This dashboard presents an analysis of **financial behaviour among university students**.
""")
st.write("""
Click a section below to view each member’s contribution.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Aisyah – Budgeting & Spending Behaviour", use_container_width=True):
        st.switch_page("page1.py")

    if st.button("🧠 Aqif – Financial Decision-Making", use_container_width=True):
        st.switch_page("page2.py")

with col2:
    if st.button("🧾 Khadijah – Consumer Rights", use_container_width=True):
        st.switch_page("page3.py")

    if st.button("🔍 Kisantini – Consumer Awareness", use_container_width=True):
        st.switch_page("page4.py")
