import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here


# DATASET UPLOAD AND SUMMARY BOX

# --- Corrected Imports ---
# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="💷Financial Behaviour among University Students",
    layout="wide" # Set layout here for consistency
)

# Forced SETUP Page Streamlit
st.markdown(
    """
    <style>
    /* Main reading area */
    .block-container {
        max-width: 900px;          /* Book-like text width */
        padding-top: 3rem;
        padding-bottom: 4rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.8;          /* Comfortable reading */
    }

    /* Improve text readability */
    p, li {
        font-size: 1.05rem;
    }

    h1, h2, h3 {
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page header
st.title("💷Financial Behaviour among University Students")
st.markdown("---")  # this creates a horizontal line
# Summary Box
col1, col2, col3, col4 = st.columns(4)

# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df

# =========================
# PLO DATA CALCULATIONS
# =========================

total_students = len(df)
# -------------------------
# PLO 1 – Cognitive Skill
# Complaint awareness level
# -------------------------
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
plo1_score = round(df['Complaint_Score'].mean(), 1)
# -------------------------
# -------------------------
# PLO 2 – Digital Skill
# Age × Complaint Behaviour
# -------------------------
# Convert Age to numeric (safety)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
# Map complaint behaviour to numeric values
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
# Calculate mean complaint score by age group
age_complaint_score = (
    df.dropna(subset=['Age', 'Complaint_Score'])
      .groupby('Age')['Complaint_Score']
      .mean()
)
# Final PLO 2 score
plo2_score = round(age_complaint_score.mean(), 1)
# -------------------------
# PLO 3 – Interpersonal Skill
# Financial Knowledge × Complaint Behaviour
# -------------------------
# Map complaint behaviour to numeric values
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
# Calculate mean complaint score by financial knowledge level
knowledge_complaint_score = (
    df.dropna(subset=['Increase_Financial_Knowledge', 'Complaint_Score'])
      .groupby('Increase_Financial_Knowledge')['Complaint_Score']
      .mean()
)
# Final PLO 3 score
plo3_score = round(knowledge_complaint_score.mean(), 1)
# -------------------------
# PLO 4 – Interpersonal Skill
# Complaint Behaviour by Monthly Income
# -------------------------
# Ensure Monthly Income is treated as string
# Map complaint behaviour to numeric values
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
# Calculate mean complaint score by monthly income group
income_complaint_score = (
    df.dropna(subset=['Monthly_Income', 'Complaint_Score'])
      .groupby('Monthly_Income')['Complaint_Score']
      .mean()
)
# Final PLO 4 score
plo4_score = round(income_complaint_score.mean(), 1)
# PLO Display
col1.metric(
    label="Complaint Behaviour",
    value=plo1_score,
    help="Calculated from complaint behaviour analysis",
    border=True
)

col2.metric(
    label="Age and Complaint",
    value=plo2_score,
    help="Calculated from digital analysis of Age and Complaint Behaviour",
    border=True
)

col3.metric(
    label="Complaint by Knowledge",
    value=plo3_score,
    help="Calculated from analysis of complaint behaviour across financial knowledge levels",
    border=True
)

col4.metric(
    label="Complaint by Income",
    value=plo4_score,
    help="Based on complaint behaviour across monthly income groups",
    border=True
)


#OBJECTIVE AND PROBLEM
st.header("🛒Consumer Rights & Complaint Behaviour")
st.markdown("---")  # this creates a horizontal line

# =========================
# 1. Individual Goal
# =========================
st.subheader("Objective")
st.write(
    """
    Study about student's awareness of consumer rights and their complaint behaviour after purchasing products.
    """
)

# =========================
# 2. Problem Definition
# =========================
st.subheader("Problem Definition")
st.write(
    """
   Even though being involved as buyers, many students might not be completely aware of their rights as consumers.
   As a result, dissatisfaction with products or services may not lead to formal complaints or refund requests.
   The Problem is, did students understand their consumer rights?
    """
)


