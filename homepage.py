import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
   .stApp {
        background-image:
            linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
            url("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Adaptive block container */
    .block-container {
        background-color: rgba(255, 255, 255, 0.8); /* fallback for light theme */
        background-color: var(--background-color-alpha); /* adapts to light/dark */
        color: var(--text-color); /* adapts text color */
        border-radius: 12px;
        padding: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="💵💷Financial Behaviour among University Students💴💶",
    layout="wide" # Set layout here for consistency
)

st.title("💵💷Financial Behaviour among University Students💴💶")
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
