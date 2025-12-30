import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# DATASET UPLOAD AND SUMMARY BOX

# --- Corrected Imports ---
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here
# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="💷Financial Behaviour among University Students",
    layout="wide" # Set layout here for consistency
)
# Page header
st.header("💷Financial Behaviour among University Students", divider="grey")

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)
# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df
# --- 2. HEADER & METRICS ---
st.header("Financial Behaviour among University Students", divider="grey")

# --- 3. GRAPH 1: PRICE COMPARISON (RESIZED) ---
st.subheader("Decision Planning Frequency")

# We create columns to "squeeze" the graph so it isn't full-width
col_left, col_mid, col_right = st.columns([1, 2, 1]) 

with col_mid:
    # Reduced figsize from (10,6) to (6,4)
    fig0, ax0 = plt.subplots(figsize=(6, 4)) 
    sns.countplot(
        data=df, 
        x='Compare_Prices_Before_Buying', 
        order=df['Compare_Prices_Before_Buying'].value_counts().index, 
        palette='viridis',
        ax=ax0
    )
    ax0.set_title('Compare Prices Before Buying', fontsize=10)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    st.pyplot(fig0)

st.divider()

# --- 4. TABS FOR REMAINING 4 GRAPHS ---
tab1, tab2, tab3, tab4 = st.tabs(["Score Distribution", "Age Analysis", "Gender Comparison", "Correlations"])

# Use a standard small size for all remaining plots
SMALL_FIG = (5, 3.5)

with tab1:
    st.write("#### Distribution of Financial Confidence")
    # Using columns inside the tab to keep it small and centered
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        fig1, ax1 = plt.subplots(figsize=SMALL_FIG)
        sns.histplot(data=df, x='Organised_Money_Management', bins=5, discrete=True, ax=ax1, color="#6A0DAD")
        st.pyplot(fig1)

with tab2:
    st.write("#### Financial Confidence Score by Age")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        fig2, ax2 = plt.subplots(figsize=SMALL_FIG)
        sns.boxplot(data=df, x='Age', y='Organised_Money_Management', palette='cubehelix', ax=ax2)
        st.pyplot(fig2)

with tab3:
    st.write("#### Average Score by Gender")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        fig3, ax3 = plt.subplots(figsize=SMALL_FIG)
        sns.barplot(data=df, x='Gender', y='Organised_Money_Management', palette='rocket', ax=ax3)
        st.pyplot(fig3)

with tab4:
    st.write("#### Correlation Heatmap")
    c1, c2, c3 = st.columns([0.5, 3, 0.5]) # Heatmap needs a bit more width for labels
    with c2:
        numerical_cols = df.select_dtypes(include=['number']).columns
        if not numerical_cols.empty:
            fig4, ax4 = plt.subplots(figsize=(7, 5))
            sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4, annot_kws={"size": 8})
            plt.xticks(fontsize=7)
            plt.yticks(fontsize=7)
            st.pyplot(fig4)
