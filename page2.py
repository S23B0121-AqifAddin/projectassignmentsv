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
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/processed_financial_capability_data.csv', encoding='latin-1')
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
    label="Financial Responsibility Index",
    value=plo1_score,
    border=True
)

col2.metric(
    label="Decision Maturity (Age)",
    value=plo2_score,
    border=True
)

col3.metric(
    label="Decision Maturity (Age)",
    value=plo3_score,
    border=True
)

col4.metric(
    label="Economic Decision Power",
    value=plo4_score,
    border=True
)


#OBJECTIVE AND PROBLEM
st.header("Financial Responsibility & Decision-Making")
st.markdown("---")  # this creates a horizontal line

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
    summary_text = "This bar chart illustrates the frequency of price-checking behavior, highlighting that a majority of students exercise market vigilance by comparing prices before making a purchase."
    st.info(summary_text)
    fig0, ax0 = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='Compare_Prices_Before_Buying', 
                  order=df['Compare_Prices_Before_Buying'].value_counts().index, 
                  palette='viridis', ax=ax0)
    plt.xticks(rotation=45, fontsize=8)
    st.pyplot(fig0)

with row1_col2:
    st.write("###### Score Distribution (Proportional)")
    summary_text = "This pie chart summarizes the composition of student confidence, revealing the part-to-whole relationship of management levels. adawiyahwanijdnwaudnwauodnwaiodwnaioadwniodnawiofnaiofnawiownai"
    st.info(summary_text)

    # 1. Prepare the data
    score_counts = df['Organised_Money_Management'].value_counts().sort_index()

    # 2. Define the Plot (Matplotlib)
    fig1, ax1 = plt.subplots(figsize=(6, 5)) # Adjusted for column fit
    
    # Use the 'magma' palette for a professional look
    colors = sns.color_palette('coolwarm', len(score_counts))
    
    ax1.pie(
        score_counts, 
        labels=score_counts.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,
        textprops={'fontsize': 10}
    )
    
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    
    # 3. Display in Streamlit
    st.pyplot(fig1)

# --- 6. BOTTOM ROW: TABS FOR DETAILED ANALYSIS ---
st.subheader("🔍 Deep Dive Analysis")
tab1, tab2= st.tabs(["Demographics (Age & Gender)", "Correlation Matrix"])

with tab1:
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.write("###### Financial Confidence by Age")
        summary_text = "This histogram illustrates the demographic spread, showing that our sample is concentrated in the early-to-mid twenties."
        st.info(summary_text)
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='Age', y='Organised_Money_Management', palette='cubehelix', ax=ax2)
        st.pyplot(fig2)
    
    with sub_col2:
        st.write("###### Average Score by Gender")
        summary_text = "This bar chart illustrates the average level of financial confidence across genders, highlighting that both males and females maintain a comparably high level of perceived competence in managing their money."
        st.info(summary_text)
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=df, x='Gender', y='Organised_Money_Management', palette='rocket', ax=ax3)
        st.pyplot(fig3)

with tab2:
    st.write("###### Feature Correlation Heatmap")
    summary_text = "This matrix summarizes the interconnectivity of habits, showing how being 'organized' is strongly linked to 'saving' and 'debt avoidance'."
    st.info(summary_text)

    # 1. REMOVED the _, mid_col, _ columns to allow the chart to use the FULL width
    numerical_cols = df.select_dtypes(include=['number']).columns
    
    if not numerical_cols.empty:
        # 2. INCREASED figsize (Width 12, Height 8) for a much bigger display
        fig4, ax4 = plt.subplots(figsize=(12, 8)) 
        
        # 3. Adjusted sns.heatmap to make annotations clearer on a larger scale
        sns.heatmap(
            df[numerical_cols].corr(), 
            annot=True, 
            cmap='coolwarm', 
            fmt=".2f", 
            ax=ax4, 
            annot_kws={"size": 10}, # Slightly larger font for numbers
            cbar_kws={'shrink': .8}  # Keeps the color bar proportional
        )
        
        # 4. Use tight_layout to prevent label overlapping
        plt.tight_layout()
        
        # 5. Use use_container_width=True to ensure it fits the Streamlit layout perfectly
        st.pyplot(fig4, use_container_width=True)
        plt.close(fig4)



st.divider()
st.write("Click a section below to view another page.")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧾 Khadijah – Consumer Rights", use_container_width=True):
        st.switch_page("page3.py")
        
    if st.button("📊 Aisyah – Budgeting & Spending Behaviour", use_container_width=True):
        st.switch_page("page1.py")

with col2:
    if st.button("🔍 Kisantini – Consumer Awareness", use_container_width=True):
        st.switch_page("page4.py")

    if st.button("👥 Group Overview", use_container_width=True):  # New button
        st.switch_page("homepage.py")  # Replace with your homepage file
