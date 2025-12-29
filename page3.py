import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# DATASET UPLOAD AND SUMMARY BOX
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
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df


# DISPLAY VISUALIZATION
#Pie Chart
# Calculate the value counts for 'Complaint_for_Unsuitable_Product'
complaint_counts = df['Complaint_for_Unsuitable_Product'].value_counts()

# Create the figure
fig, ax = plt.subplots(figsize=(4, 4))
colors = plt.cm.Set3.colors  # Distinct qualitative colormap

ax.pie(
    complaint_counts,
    labels=complaint_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors
)

ax.set_title('Distribution of Complaint Behavior for Unsuitable Products')
ax.axis('equal')  # Ensures pie is a circle

# Display in Streamlit
st.pyplot(fig)
