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
    data = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
data

# Tajuk aplikasi
st.title("Correlation Heatmap of Financial Attitudes")

# Load dataset dari GitHub
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/main/processed_financial_capability_data.csv"
data = pd.read_csv(url)

# Senarai kolum sikap kewangan
attitude_columns = [
    'Organised_Money_Management',
    'Saver_or_Spender',
    'Buy_on_Credit',
    'Avoid_Credit_Debt',
    'Savings_for_Rainy_Day',
    'Pension_Funds_for_Retirement',
    'Live_for_Today',
    'Savings_for_Life_Changes',
    'Plan_for_Old_Age_Care'
]

# Kira correlation matrix
correlation_matrix = data[attitude_columns].corr()

# Plot heatmap
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    linewidths=.5,
    ax=ax
)

ax.set_title('Correlation Heatmap of Financial Attitudes')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

# Papar dalam Streamlit
st.pyplot(fig)

# Tajuk aplikasi
st.title("Distribution of Monthly Income")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

sns.countplot(
    x='Monthly_Income',
    data=data,
    order=data['Monthly_Income'].value_counts().index,
    hue='Monthly_Income',
    palette='viridis',
    legend=False,
    ax=ax
)

ax.set_title('Distribution of Monthly Income')
ax.set_xlabel('Monthly Income')
ax.set_ylabel('Count')
plt.tight_layout()

# Papar graf dalam Streamlit
st.pyplot(fig)

# Tajuk aplikasi
st.title("Relationship between Budget Following and Monthly Savings")

# Crosstab (normalize ikut baris / index)
budget_savings_crosstab = pd.crosstab(
    data['Has_Budget'],
    data['Monthly_Savings'],
    normalize='index'
)

# Plot stacked bar chart
fig, ax = plt.subplots(figsize=(10, 6))
budget_savings_crosstab.plot.bar(
    stacked=True,
    colormap='viridis',
    ax=ax
)

ax.set_title('Relationship between Budget Following and Monthly Savings')
ax.set_xlabel('Follow Budget')
ax.set_ylabel('Proportion of Monthly Savings')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.legend(title='Monthly Savings')

plt.tight_layout()

# Papar graf dalam Streamlit
st.pyplot(fig)
