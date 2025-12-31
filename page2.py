import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. PAGE CONFIG (Must be first)
st.set_page_config(
    page_title="💷 Financial Behaviour Dashboard",
    layout="wide"
)

# Custom CSS for readability
st.markdown(
    """
    <style>
    .block-container { max-width: 1000px; padding-top: 2rem; }
    p, li { font-size: 1.05rem; line-height: 1.6; }
    </style>
    """,
    unsafe_allow_html=True
)

# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df

# 3. CALCULATIONS (Prepare data for metrics)
mapping = {'Never': 1, 'Sometimes': 3, 'Always': 5}
df['Responsibility_Score'] = df['Complaint_for_Unsuitable_Product'].map(mapping)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

p1 = round(df['Responsibility_Score'].mean(), 1)
p2 = round(df.dropna(subset=['Age', 'Responsibility_Score']).groupby('Age')['Responsibility_Score'].mean().mean(), 1)
p3 = round(df.dropna(subset=['Increase_Financial_Knowledge', 'Responsibility_Score']).groupby('Increase_Financial_Knowledge')['Responsibility_Score'].mean().mean(), 1)
p4 = round(df.dropna(subset=['Monthly_Income', 'Responsibility_Score']).groupby('Monthly_Income')['Responsibility_Score'].mean().mean(), 1)

# 4. HEADER & SUMMARY BOX (Displayed First)
st.title("💷 Financial Behaviour among University Students")
st.markdown("---")

# Metrics appear right at the top
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Financial Responsibility Index", p1, border=True)
m_col2.metric("Decision Maturity (Age)", p2, border=True)
m_col3.metric("Knowledge-Driven Actions", p3, border=True)
m_col4.metric("Economic Decision Power", p4, border=True)

st.markdown("---")

# 5. OBJECTIVES & PROBLEM
st.subheader("Objective")
st.write("To investigate how financial responsibility influences decision-making in university students...")

st.subheader("Problem Definition")
st.write("University students exhibit poor financial responsibility, marked by impulsive decisions...")

st.divider()

# 6. KEY BEHAVIOURAL INSIGHTS
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
    plt.close(fig0)

with row1_col2:
    st.write("###### Score Distribution")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x='Organised_Money_Management', bins=5, discrete=True, color="#6A0DAD", ax=ax1)
    ax1.set_xticks(range(1, 6))
    st.pyplot(fig1)
    plt.close(fig1)

# 7. DEEP DIVE TABS
st.subheader("🔍 Deep Dive Analysis")
tab1, tab2, tab3 = st.tabs(["Demographics", "Correlation", "Raw Dataset"])

with tab1:
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.write("###### Financial Confidence by Age")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='Age', y='Organised_Money_Management', palette='cubehelix', ax=ax2)
        st.pyplot(fig2)
        plt.close(fig2)
    with sub_col2:
        st.write("###### Average Score by Gender")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=df, x='Gender', y='Organised_Money_Management', palette='rocket', ax=ax3)
        st.pyplot(fig3)
        plt.close(fig3)

with tab2:
    st.write("###### Feature Correlation Heatmap")
    # Using a diagram tag to help you visualize the expected outcome
    
    num_cols = df.select_dtypes(include=['number']).columns
    if not num_cols.empty:
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
        st.pyplot(fig4)
        plt.close(fig4)

with tab3:
    st.dataframe(df, use_container_width=True)
