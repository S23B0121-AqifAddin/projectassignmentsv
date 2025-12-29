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

# 1. Setup Page
st.set_page_config(page_title="Consumer Awareness Dashboard", layout="wide")

# 2. Sidebar Filters
st.sidebar.header("Data Controls")

# Gender Filter
gender_options = df_awareness['Gender'].unique().tolist()
selected_genders = st.sidebar.multiselect("Filter by Gender:", gender_options, default=gender_options)

# Age Filter (Assuming an 'Age_Group' column exists)
age_options = df_awareness['Age_Group'].unique().tolist()
selected_ages = st.sidebar.multiselect("Filter by Age Group:", age_options, default=age_options)

# Apply Filters to the Dataframe
filtered_df = df_awareness[
    (df_awareness['Gender'].isin(selected_genders)) & 
    (df_awareness['Age_Group'].isin(selected_ages))
]

# 3. Main Header & Download Button
st.title("Consumer Behavior & Awareness Analysis")

# Convert filtered dataframe to CSV for download
csv_data = filtered_df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name='filtered_consumer_data.csv',
    mime='text/csv',
)

# 4. Visualization Logic
def create_plot(column, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=filtered_df, x=column, palette='viridis', ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# 5. Dashboard Grid
col1, col2 = st.columns(2)

with col1:
    create_plot('Search_Info_Before_Buying', 'Search Info Before Buying')
    create_plot('Compare_Prices_Before_Buying', 'Compare Prices Before Buying')

with col2:
    create_plot('Compare_Products_Services', 'Compare Products/Services')
    create_plot('Read_Agreement_Carefully', 'Read Agreement Carefully')

# 6. Data Summary Section
st.divider()
st.subheader("Data Overview")
st.write(f"Showing **{len(filtered_df)}** records based on current filters.")
if st.checkbox("Show Data Table"):
    st.dataframe(filtered_df, use_container_width=True)
