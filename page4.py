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
