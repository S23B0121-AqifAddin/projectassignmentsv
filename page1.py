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

# Title Bar Chart
st.title("Distribution of Monthly Income Range")

# Load data 
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/main/processed_financial_capability_data.csv"
data = pd.read_csv(url)

# Check column name
st.write("Dataset Preview:")
st.dataframe(data.head())

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

sns.countplot(
    y='Monthly_Income',
    data=data,
    order=data['Monthly_Income'].value_counts().index,
    palette='viridis',
    ax=ax
)

ax.set_title('Distribution of Monthly Income Range')
ax.set_xlabel('Count')
ax.set_ylabel('Monthly Income Range')

st.pyplot(fig)


