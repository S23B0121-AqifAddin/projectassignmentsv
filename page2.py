import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# --- Corrected Imports ---
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here

# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Financial Behaviour among University Students",
    layout="wide" # Set layout here for consistency
)

# Page header
st.header("Financial Behaviour among University Students", divider="grey")

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

# Load your data
try:
    df2 = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df2 = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df2

#OBJECTIVE, PROBLEM AND VARIABLE USED
st.header("Financial Capability and Consumer Behaviour among University Students)

# =========================
# 1. Individual Goal
# =========================
st.subheader("Objective")
st.write(
    """
    To evaluate the financial capability of university students and analyze its influence on their consumer behavior patterns, 
    identifying key gaps in knowledge and decision-making via survey data.
    """
)

# =========================
# 2. Problem Definition
# =========================
st.subheader("Problem Definition")
st.write(
    """
   University students' low financial literacy creates a pressing problem of poor money management, which this case study addresses through targeted analysis. 
   Its relevance to industries stems from actionable insights for better products and policies, while scientific visualization is justified by its ability to reveal patterns efficiently.
    """
)


# Create the countplot
    sns.countplot(
        data=data, 
        x='Compare_Prices_Before_Buying', 
        order=data['Compare_Prices_Before_Buying'].value_counts().index, 
        palette='viridis',
        ax=ax  # It is best practice to specify the axis in Streamlit
    )
    
    # Customizing labels
    ax.set_title('Decision Planning Frequency (Compare Prices Before Buying)', fontsize=14)
    ax.set_xlabel('Response', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # 4. Display the plot in Streamlit
    st.pyplot(fig)

# Call the function
if 'df' in locals() or 'df' in globals():
    plot_price_comparison(df)
else:
    st.error("Dataframe 'df' not found. Please ensure your data is loaded.")

# Use tabs to organize the different charts
tab1, tab2, tab3, tab4 = st.tabs(["Score Distribution", "Age Analysis", "Gender Comparison", "Correlations"])

# --- TAB 1: Histogram ---
with tab1:
    st.subheader("Distribution of Financial Confidence")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(
        data=df, 
        x='Organised_Money_Management', 
        bins=5, 
        kde=False, 
        palette='magma', 
        discrete=True, 
        ax=ax1
    )
    ax1.set_title('Distribution of Financial Confidence Score', fontsize=14)
    ax1.set_xlabel('Organised Money Management Score (1-5)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_xticks(range(1, 6))
    plt.tight_layout()
    st.pyplot(fig1)

# --- TAB 2: Boxplot ---
with tab2:
    st.subheader("Financial Confidence by Age Group")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=df, 
        x='Age', 
        y='Organised_Money_Management', 
        palette='cubehelix', 
        ax=ax2
    )
    ax2.set_title('Financial Confidence Score by Age', fontsize=14)
    ax2.set_xlabel('Age', fontsize=12)
    ax2.set_ylabel('Score', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig2)

# --- TAB 3: Barplot ---
with tab3:
    st.subheader("Gender-Based Score Averages")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=df, 
        x='Gender', 
        y='Organised_Money_Management', 
        palette='rocket', 
        ax=ax3
    )
    ax3.set_title('Average Financial Confidence Score by Gender', fontsize=14)
    ax3.set_xlabel('Gender', fontsize=12)
    ax3.set_ylabel('Average Score', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig3)

# --- TAB 4: Heatmap ---
with tab4:
    st.subheader("Feature Correlation Matrix")
    # Ensure numerical_cols exists
    if 'numerical_cols' in locals() or 'numerical_cols' in globals():
        correlation_matrix = df[numerical_cols].corr()
        fig4, ax4 = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            correlation_matrix, 
            annot=True, 
            cmap='coolwarm', 
            fmt=".2f", 
            linewidths=.5, 
            ax=ax4
        )
        ax4.set_title('Correlation Heatmap of Numerical Features', fontsize=16)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig4)
    else:
        st.warning("Please define 'numerical_cols' to view the heatmap.")


