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
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='latin-1')
df

# =========================
# PLO DATA CALCULATIONS
# =========================

total_students = len(df)
# -------------------------
# PLO 1 – Cognitive Skill
# Complaint awareness level
# -------------------------
# 3. CALCULATIONS (Prepare data for metrics)
mapping = {'Never': 1, 'Sometimes': 3, 'Always': 5}
df['Responsibility_Score'] = df['Complaint_for_Unsuitable_Product'].map(mapping)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

p1 = round(df['Responsibility_Score'].mean(), 1)
p2 = round(df.dropna(subset=['Age', 'Responsibility_Score']).groupby('Age')['Responsibility_Score'].mean().mean(), 1)
p3 = round(df.dropna(subset=['Increase_Financial_Knowledge', 'Responsibility_Score']).groupby('Increase_Financial_Knowledge')['Responsibility_Score'].mean().mean(), 1)
p4 = round(df.dropna(subset=['Monthly_Income', 'Responsibility_Score']).groupby('Monthly_Income')['Responsibility_Score'].mean().mean(), 1)

# Metrics appear right at the top
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Financial Responsibility ndex", p1, border=True)
m_col2.metric("Decision Maturity (Age)", p2, border=True)
m_col3.metric("Knowledge-Driven Actions", p3, border=True)
m_col4.metric("Economic Decision Power", p4, border=True)

# =========================
# 1. Individual Goal
# =========================
st.subheader("Objective")
st.write(
    """
    To investigate how financial responsibility influences decision-making in university students, evaluating literacy levels, spending patterns, 
    and risk factors through survey analysis for targeted interventions.

    """
)

# =========================
# 2. Problem Definition
# =========================
st.subheader("Problem Definition")
st.write(
    """
   University students exhibit poor financial responsibility, marked by impulsive decisions like credit misuse and overspending, due to inadequate knowledge of budgeting and investments. 
   This results in debt burdens (e.g., 40%+ with loans struggle), food insecurity, and long-term unpreparedness, exacerbated by limited education access.

    """
)

st.divider()

# --- 5. TOP ROW: BEHAVIORAL OVERVIEW (RESIZED SIDE-BY-SIDE) ---
st.subheader("📊 Key Behavioural Insights")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write("###### Price Comparison Frequency")
    fig0, ax0 = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='Compare_Prices_Before_Buying', 
                  order=df['Compare_Prices_Before_Buying'].value_counts().index, 
                  palette='viridis', ax=ax0)
    plt.xticks(rotation=45, fontsize=8)
    st.pyplot(fig0)

with row1_col2:
    st.write("###### Score Distribution")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x='Organised_Money_Management', bins=5, discrete=True, color="#6A0DAD", ax=ax1)
    ax1.set_xticks(range(1, 6))
    st.pyplot(fig1)

# --- 6. BOTTOM ROW: TABS FOR DETAILED ANALYSIS ---
st.subheader("🔍 Deep Dive Analysis")
tab1, tab2, tab3 = st.tabs(["Demographics (Age & Gender)", "Correlation Matrix", "Raw Dataset"])

with tab1:
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.write("###### Financial Confidence by Age")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='Age', y='Organised_Money_Management', palette='cubehelix', ax=ax2)
        st.pyplot(fig2)
    
    with sub_col2:
        st.write("###### Average Score by Gender")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=df, x='Gender', y='Organised_Money_Management', palette='rocket', ax=ax3)
        st.pyplot(fig3)

with tab2:
    st.write("###### Feature Correlation Heatmap")
    # Centering the heatmap to keep it from stretching
    _, mid_col, _ = st.columns([1, 4, 1])
    with mid_col:
        numerical_cols = df.select_dtypes(include=['number']).columns
        if not numerical_cols.empty:
            fig4, ax4 = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4, annot_kws={"size": 8})
            st.pyplot(fig4)

with tab3:
    st.dataframe(df, use_container_width=True)

