import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Financial Behaviour Dashboard",
    layout="wide"
)

# Page header
st.title("💷 Financial Behaviour Analysis: University Students")
st.markdown("Comprehensive view of Financial Responsibility and Decision-Making.")
st.markdown("---")

# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df

# 3. CALCULATIONS
responsibility_mapping = {'Never': 1, 'Sometimes': 3, 'Always': 5}
df['Responsibility_Score'] = df['Complaint_for_Unsuitable_Product'].map(responsibility_mapping)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

plo1 = round(df['Responsibility_Score'].mean(), 1)
plo2 = round(df.dropna(subset=['Age', 'Responsibility_Score']).groupby('Age')['Responsibility_Score'].mean().mean(), 1)
plo3 = round(df.dropna(subset=['Increase_Financial_Knowledge', 'Responsibility_Score']).groupby('Increase_Financial_Knowledge')['Responsibility_Score'].mean().mean(), 1)
plo4 = round(df.dropna(subset=['Monthly_Income', 'Responsibility_Score']).groupby('Monthly_Income')['Responsibility_Score'].mean().mean(), 1)

# 4. TOP METRICS ROW
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Financial Responsibility Index", plo1, help="Overall average responsibility score.", border=True)
m_col2.metric("Decision Maturity (Age)", plo2, help="Responsibility score normalized by age.", border=True)
m_col3.metric("Knowledge-Driven Actions", plo3, help="Impact of financial knowledge on behavior.", border=True)
m_col4.metric("Economic Decision Power", plo4, help="Responsibility levels across income brackets.", border=True)

st.markdown("---")

# 5. SEPARATED VISUALIZATIONS

# --- SECTION 1: DEMOGRAPHICS ---
with st.container(border=True):
    st.subheader("1. Student Demographics")
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.write("**Age Distribution**")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.histplot(df['Age'], kde=True, color='teal', ax=ax1)
        st.pyplot(fig1)
        plt.close(fig1)

    with row1_col2:
        st.write("**Gender Distribution**")
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        gender_counts = df['Gender'].value_counts()
        ax2.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        st.pyplot(fig2)
        plt.close(fig2)

# --- SECTION 2: BEHAVIORAL ANALYSIS ---
with st.container(border=True):
    st.subheader("2. Behavioral & Responsibility Analysis")
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.write("**Responsibility Distribution (Complaint Behavior)**")
        complaint_counts = df['Complaint_for_Unsuitable_Product'].value_counts()
        fig3, ax3 = plt.subplots(figsize=(6, 6))
