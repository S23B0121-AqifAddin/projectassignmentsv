import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. SET UP PAGE ---
st.set_page_config(
    page_title="Financial Behaviour among University Students",
    layout="wide"
)

# Page header
st.header("Financial Behaviour among University Students", divider="grey")

# Metrics Section
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="PLO 2", value="3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value="3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value="4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value="4.3", help="PLO 5: Communication Skill", border=True)

# --- 2. LOAD DATA ---
@st.cache_data # Cache data to make the app faster
def load_data():
    url = 'https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv'
    try:
        data = pd.read_csv(url, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(url, encoding='latin-1')
    return data

df = load_data()

# Show raw data (optional)
with st.expander("View Raw Dataset"):
    st.write(df)

# --- 3. OBJECTIVES & PROBLEM ---
st.header("Financial Capability and Consumer Behaviour among University Students")

obj_col, prob_col = st.columns(2)
with obj_col:
    st.subheader("Objective")
    st.info("To evaluate the financial capability of university students and analyze its influence on their consumer behavior patterns.")

with prob_col:
    st.subheader("Problem Definition")
    st.warning("University students' low financial literacy creates a pressing problem of poor money management.")

# --- 4. PRICE COMPARISON CHART ---
def plot_price_comparison(data):
    st.subheader("Decision Planning Frequency")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(
        data=data, 
        x='Compare_Prices_Before_Buying', 
        order=data['Compare_Prices_Before_Buying'].value_counts().index, 
        palette='viridis',
        ax=ax
    )
    ax.set_title('Compare Prices Before Buying', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

plot_price_comparison(df)

# --- 5. TABS FOR DETAILED ANALYSIS ---
st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["Score Distribution", "Age Analysis", "Gender Comparison", "Correlations"])

# TAB 1: Histogram
with tab1:
    st.subheader("Distribution of Financial Confidence")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='Organised_Money_Management', bins=5, palette='magma', discrete=True, ax=ax1)
    ax1.set_xticks(range(1, 6))
    st.pyplot(fig1)

# TAB 2: Boxplot
with tab2:
    st.subheader("Financial Confidence by Age Group")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Age', y='Organised_Money_Management', palette='cubehelix', ax=ax2)
    st.pyplot(fig2)

# TAB 3: Barplot
with tab3:
    st.subheader("Gender-Based Score Averages")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x='Gender', y='Organised_Money_Management', palette='rocket', ax=ax3)
    st.pyplot(fig3)

# TAB 4: Heatmap
with tab4:
    st.subheader("Feature Correlation Matrix")
    numerical_cols = df.select_dtypes(include=['number']).columns
    if not numerical_cols.empty:
        fig4, ax4 = plt.subplots(figsize=(12, 10))
        sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
        st.pyplot(fig4)
    else:
        st.write("No numerical columns found for correlation.")
