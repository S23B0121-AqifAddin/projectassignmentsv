import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here


# DATASET UPLOAD AND SUMMARY BOX

# --- Corrected Imports ---
# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="💷Financial Behaviour among University Students",
    layout="wide" # Set layout here for consistency
)
# Page header
st.title("💷Financial Behaviour among University Students")

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

#OBJECTIVE, PROBLEM AND VARIABLE USED
st.header("🛒Consumer Rights & Complaint Behaviour", divider="purple")

# =========================
# 1. Individual Goal
# =========================
st.subheader("Objective")
st.write(
    """
    Study about student's awareness of consumer rights and their complaint behaviour after purchasing products.
    """
)

# =========================
# 2. Problem Definition
# =========================
st.subheader("Problem Definition")
st.write(
    """
   Even though being involved as buyers, many students might not be completely aware of their rights as consumers.
   As a result, dissatisfaction with products or services may not lead to formal complaints or refund requests.
   The Problem is, did students understand their consumer rights?
    """
)


# DISPLAY VISUALIZATION

#Heatmap
st.subheader("Correlation of Financial Management and Planning Behaviours")
st.write(
    "This heatmap illustrates the strength and direction of relationships among financial "
    "management and planning behaviours. Strong positive correlations suggest behaviours "
    "that tend to occur together, while negative correlations indicate contrasting habits."
)
# Select numerical columns related to financial management and planning behaviors
selected_numerical_cols = [
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
# Calculate correlation matrix
correlation_matrix = df[selected_numerical_cols].corr()
# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    linewidths=0.5,
    ax=ax
)

ax.set_title('Correlation Heatmap of Financial Management and Planning Behaviors')

plt.tight_layout()
# Display in Streamlit
st.pyplot(fig)

#Pie Chart
st.subheader("Complaint Behavior for Unsuitable Products")
st.write("This pie chart shows the proportion of consumers who submit complaints regarding unsuitable products.")
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

#Violin Plot
st.subheader("Age Distribution and Complaint Behaviour")
st.write(
    "The violin plot illustrates how age is distributed among consumers who did and did not "
    "file complaints regarding unsuitable products, highlighting differences in complaint patterns."
)
# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

sns.violinplot(
    x='Complaint_for_Unsuitable_Product',
    y='Age',
    data=df,
    hue='Complaint_for_Unsuitable_Product',
    palette='viridis',
    legend=False,
    ax=ax
)

ax.set_title('Age Distribution by Complaint Behavior for Unsuitable Products (Violin Plot)')
ax.set_xlabel('Complaint_for_Unsuitable_Product')
ax.set_ylabel('Age')

plt.tight_layout()
# Display in Streamlit
st.pyplot(fig)

#Grouped Bar Plot
st.subheader("Complaint Behaviour by Gender")
st.write(
    "This bar chart compares complaint behaviour for unsuitable products across genders, "
    "highlighting potential differences in reporting patterns."
)
# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

sns.countplot(
    x='Complaint_for_Unsuitable_Product',
    hue='Gender',
    data=df,
    palette='viridis',
    ax=ax
)

ax.set_title('Complaint Behavior by Gender')
ax.set_xlabel('Complaint_for_Unsuitable_Product')
ax.set_ylabel('Count')

plt.tight_layout()
# Display in Streamlit
st.pyplot(fig)

#Stacked Bar Plot
st.subheader("Financial Knowledge Increase vs Complaint Behaviour")
st.write(
    "This stacked percentage bar chart shows how complaint behaviour for unsuitable products "
    "varies across different levels of financial knowledge improvement. The proportions allow "
    "for direct comparison between categories."
)
# Create a cross-tabulation (contingency table)
contingency_table = pd.crosstab(
    df['Increase_Financial_Knowledge'],
    df['Complaint_for_Unsuitable_Product']
)
# Normalize to proportions (stacked percentage bar chart)
contingency_table_normalized = contingency_table.div(
    contingency_table.sum(axis=1), axis=0
)
# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

contingency_table_normalized.plot(
    kind='bar',
    stacked=True,
    colormap='viridis',
    ax=ax
)

ax.set_title('Complaint Behavior by Financial Knowledge Increase')
ax.set_xlabel('Increase_Financial_Knowledge')
ax.set_ylabel('Proportion')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

ax.legend(
    title='Complaint_for_Unsuitable_Product',
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

plt.tight_layout()
# Display in Streamlit
st.pyplot(fig)

#Faceted Bar Plot
st.subheader("Complaint Behaviour by Monthly Income")
st.write(
    "These faceted bar charts compare complaint behaviour for unsuitable products "
    "across different monthly income groups. Sharing the y-axis allows for clearer "
    "comparison of complaint frequency between income categories."
)
# Define category orders
monthly_income_order = ['Below RM 99', 'RM 100 - RM 500', 'Above RM 600']
complaint_order = ['Never', 'Sometimes', 'Always']
# Create faceted count plot
g = sns.catplot(
    data=df,
    x='Complaint_for_Unsuitable_Product',
    col='Monthly_Income',
    kind='count',
    col_order=monthly_income_order,
    order=complaint_order,
    height=5,
    aspect=1,
    palette='viridis',
    sharey=True
)

g.set_axis_labels('Complaint Behavior', 'Count')
g.set_titles('Monthly Income: {col_name}')
# Overall title
g.fig.suptitle(
    'Complaint Behavior by Monthly Income (Faceted Bar Plots)',
    y=1.05
)
# Display in Streamlit
st.pyplot(g.fig)
