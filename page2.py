import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Financial Behaviour Study",
    layout="wide"
)

# 2. DATA LOADING
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv'
    try:
        return pd.read_csv(url, encoding='utf-8')
    except:
        return pd.read_csv(url, encoding='latin-1')

df = load_data()

# 3. HEADER & METRICS
st.header("Financial Behaviour among University Students", divider="grey")

col1, col2, col3, col4 = st.columns(4)
col1.metric("PLO 2", "3.3", help="Cognitive Skill", border=True)
col2.metric("PLO 3", "3.5", help="Digital Skill", border=True)
col3.metric("PLO 4", "4.0", help="Interpersonal Skill", border=True)
col4.metric("PLO 5", "4.3", help="Communication Skill", border=True)

# 4. OBJECTIVES
st.subheader("Objective")
st.write("To evaluate the financial capability of university students and analyze its influence on behavior.")

# 5. VISUALIZATIONS
# Plot 1: Price Comparison (Outside Tabs)
st.write("### Decision Planning Frequency")
fig0, ax0 = plt.subplots(figsize=(10, 5))
sns.countplot(
    data=df, 
    x='Compare_Prices_Before_Buying', 
    order=df['Compare_Prices_Before_Buying'].value_counts().index, 
    palette='viridis',
    ax=ax0
)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig0)

# Tabs for other plots
tab1, tab2, tab3, tab4 = st.tabs(["Score Distribution", "Age Analysis", "Gender Comparison", "Correlations"])

with tab1:
    fig1, ax1 = plt.subplots()
    sns.histplot(data=df, x='Organised_Money_Management', bins=5, discrete=True, ax=ax1)
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=df, x='Age', y='Organised_Money_Management', ax=ax2)
    st.pyplot(fig2)

with tab3:
    fig3, ax3 = plt.subplots()
    sns.barplot(data=df, x='Gender', y='Organised_Money_Management', ax=ax3)
    st.pyplot(fig3)

with tab4:
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        fig4, ax4 = plt.subplots(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax4)
        st.pyplot(fig4)
