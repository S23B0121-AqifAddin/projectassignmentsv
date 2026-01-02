import streamlit as st
import pandas as pd

#SETUP SETTING
st.markdown(
    """
    <style>
   /* Full background image for the page */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e");
        background-size: cover;
        background-position: center;
    }

    /* Transparent black box behind the title */
    .title-box {
        background-color: rgba(0, 0, 0, 0.5);  /* Transparent black */
        padding: 20px 40px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 50px;
    }

    .title-box h1 {
        color: white;   /* Title text color */
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
    }

    /* Center the title box */
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display title inside transparent black box
st.markdown(
    """
    <div class="title-container">
        <div class="title-box">
            <h1>Financial Behaviour among University Students</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#PAGE
# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="💵💷Financial Behaviour among University Students💴💶",
    layout="wide" # Set layout here for consistency
)

st.markdown('<div class="custom-title">💵💷Financial Behaviour among University Students💴💶</div>', unsafe_allow_html=True)
st.markdown("---")

st.header("📈📉Original Dataset(Without Cleaning)")
#Load Original Dataset
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='latin-1')
df
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
