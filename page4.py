import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Consumer Awareness & Information Seeking",
    layout="wide"
)

st.header("Consumer Awareness & Information Seeking", divider="grey")
st.subheader("Before Buying Behaviour among University Students")

st.write(
    "This section examines students’ consumer awareness and information-seeking behaviour "
    "before making purchasing decisions. The analysis focuses on whether students actively "
    "seek information, compare alternatives, and read important product details prior to buying."
)

# ==================================================
# LOAD DATASET
# ==================================================
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv"
df = pd.read_csv(url)

# VARIABLES (BEFORE BUYING)

# Mapping to dataset columns:
# - Reading product information → Read_Agreement_Carefully
# - Comparing alternatives → Compare_Products_Services
# - Seeking information → Search_Info_Before_Buying
# - Comparing prices → Compare_Prices_Before_Buying

awareness_cols = [
    "Compare_Prices_Before_Buying",
    "Search_Info_Before_Buying",
    "Read_Agreement_Carefully",
    "Compare_Products_Services",
    "Increase_Financial_Knowledge",
    "Complaint_for_Unsuitable_Product",
    "Age",
    "Faculty"
]

# 3. Create/Filter the dataframe
# (Assuming 'df' is already loaded in your environment)
df_awareness = df[awareness_cols]

# 4. Display Descriptive Statistics
st.subheader("Descriptive Statistics")
st.dataframe(df_awareness.describe())

# 5. Optional: Add a toggle to see the raw data
if st.checkbox("Show raw awareness data"):
    st.write(df_awareness)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Consumer Behavior Dashboard", layout="wide")

st.title("📊 Consumer Awareness Analysis")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
# Replace 'Gender' with any actual column name in your df_awareness
gender_list = df_awareness['Gender'].unique().tolist()
selected_gender = st.sidebar.multiselect("Select Gender", gender_list, default=gender_list)

# Filter the dataframe based on selection
filtered_df = df_awareness[df_awareness['Gender'].isin(selected_gender)]

# --- REUSABLE PLOTTING FUNCTION ---
def render_chart(column, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=filtered_df, x=column, palette='viridis', ax=ax)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# --- 2x2 GRID LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    render_chart('Search_Info_Before_Buying', '1. Searching Product Info')
    render_chart('Compare_Prices_Before_Buying', '3. Comparing Prices')

with col2:
    render_chart('Compare_Products_Services', '2. Comparing Alternatives')
    render_chart('Read_Agreement_Carefully', '4. Reading Agreements')

# Optional: Show raw data if the user wants
if st.checkbox("Show Raw Filtered Data"):
    st.dataframe(filtered_df)
