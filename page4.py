import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title="Consumer Awareness Dashboard", layout="wide")

# Page header
st.header("Financial Behaviour among University Students", divider="grey")

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

# Load your data
try:
    dfkisa = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Kisa)processed_financial_capability_data%20(3).csv', encoding='utf-8')
except UnicodeDecodeError:
    dfkisa = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Kisa)processed_financial_capability_data%20(3).csv', encoding='latin-1')

dfraw = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv')

# Sidebar Filters
st.sidebar.header("Data Controls")

# Gender Filter
gender_options = dfraw["Gender"].dropna().unique().tolist()
selected_genders = st.sidebar.multiselect(
    "Filter by Gender:",
    gender_options,
    default=gender_options
)

# Age Filter (use Age column)
age_options = dfraw["Age"].dropna().unique().tolist()
selected_ages = st.sidebar.multiselect(
    "Filter by Age:",
    age_options,
    default=age_options
)

# Apply Filters
filtered_df = dfraw[
    (dfraw["Gender"].isin(selected_genders)) &
    (dfraw["Age"].isin(selected_ages))
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
