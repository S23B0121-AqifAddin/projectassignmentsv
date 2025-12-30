import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. SETUP & DATA LOADING ---
st.set_page_config(page_title="Financial Behaviour Dashboard", layout="wide")

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv'
    try:
        return pd.read_csv(url, encoding='utf-8')
    except:
        return pd.read_csv(url, encoding='latin-1')

df = load_data()

# --- 2. HEADER SECTION ---
st.header("Financial Capability Analysis", divider="grey")

# --- 3. THE TABS SECTION (Your Charts Go Here) ---
tab1, tab2, tab3 = st.tabs(["Age & Gender Analysis", "Correlation Heatmap", "Raw Data"])

# --- TAB 1: Boxplot and Barplot ---
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Financial Confidence by Age")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df, x='Age', y='Organised_Money_Management', palette='cubehelix', ax=ax1)
        ax1.set_title('Financial Confidence Score by Age')
        st.pyplot(fig1)

    with col_b:
        st.subheader("Average Score by Gender")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='Gender', y='Organised_Money_Management', palette='rocket', ax=ax2)
        ax2.set_title('Average Financial Confidence Score by Gender')
        st.pyplot(fig2)

# --- TAB 2: Heatmap ---
with tab2:
    st.subheader("Correlation of Numerical Features")
    
    # Automatically identify numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    
    if not numerical_cols.empty:
        correlation_matrix = df[numerical_cols].corr()
        fig3, ax3 = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            correlation_matrix, 
            annot=True, 
            cmap='coolwarm', 
            fmt=".2f", 
            linewidths=.5, 
            ax=ax3
        )
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig3)
    else:
        st.error("No numerical columns found to generate a heatmap.")

# --- TAB 3: Data Table ---
with tab3:
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)
