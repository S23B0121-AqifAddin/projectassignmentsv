import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. PAGE CONFIG
st.set_page_config(
    page_title="💷 Financial Behaviour Dashboard",
    layout="wide"
)

# Page header
st.title("💷 Financial Behaviour Analysis: University Students")
st.markdown("Comprehensive view of Financial Responsibility and Decision-Making.")
st.markdown("---")

# 2. DATASET LOADING
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv'
    try:
        data = pd.read_csv(url, encoding='utf-8')
    except:
        data = pd.read_csv(url, encoding='latin-1')
    return data

df = load_data()

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

# =========================================================
# ALL VISUALIZATIONS (DISPLAYED SIMULTANEOUSLY)
# =========================================================

# ROW 1: Basic Demographics
st.subheader("1. Student Demographics")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write("**Age Distribution**")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.histplot(df['Age'], kde=True, color='teal', ax=ax1)
    st.pyplot(fig1)

with row1_col2:
    st.write("**Gender Distribution**")
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    gender_counts = df['Gender'].value_counts()
    ax2.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
    st.pyplot(fig2)

st.markdown("---")

# ROW 2: Behavioral Analysis
st.subheader("2. Behavioral & Responsibility Analysis")
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.write("**Responsibility Distribution (Complaint Behavior)**")
    complaint_counts = df['Complaint_for_Unsuitable_Product'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(complaint_counts, labels=complaint_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('viridis'))
    st.pyplot(fig3)

with row2_col2:
    st.write("**Maturity Analysis (Age vs. Responsibility)**")
    
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.violinplot(x='Complaint_for_Unsuitable_Product', y='Age', data=df, palette='muted', ax=ax4)
    st.pyplot(fig4)

st.markdown("---")

# ROW 3: Correlation & Economic Factors
st.subheader("3. Correlation & Economic Decision Power")
row3_col1, row3_col2 = st.columns([2, 1]) # Make heatmap column wider

with row3_col1:
    st.write("**Correlation of Financial Behaviours**")
    

[Image of a correlation matrix heatmap]

    selected_cols = [
        'Organised_Money_Management', 'Saver_or_Spender', 'Buy_on_Credit',
        'Avoid_Credit_Debt', 'Savings_for_Rainy_Day', 'Pension_Funds_for_Retirement'
    ]
    corr = df[selected_cols].corr()
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax5)
    st.pyplot(fig5)

with row3_col2:
    st.write("**Income vs. Responsibility**")
    income_order = ['Below RM 99', 'RM 100 - RM 500', 'Above RM 600']
    ct = pd.crosstab(df['Monthly_Income'], df['Complaint_for_Unsuitable_Product']).reindex(income_order)
    ct_norm = ct.div(ct.sum(1), axis=0)
    fig6, ax6 = plt.subplots(figsize=(6, 10))
    ct_norm.plot(kind='bar', stacked=True, ax=ax6, colormap='viridis')
    st.pyplot(fig6)

# ============= OBJECTIVES =============
st.markdown("---")
with st.expander("View Project Context"):
    st.write("**Objective:** Study awareness of consumer rights and complaint behaviour.")
    st.write("**Problem:** Dissatisfaction does not always lead to action. This dashboard explores how demographics and knowledge bridge that gap.")
