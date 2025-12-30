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
st.markdown("---")  # this creates a horizontal line
# Summary Box
col1, col2, col3, col4 = st.columns(4)

# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df

# =========================
# PLO DATA CALCULATIONS
# =========================

total_students = len(df)
# -------------------------
# PLO 2 – Cognitive Skill
# Complaint awareness level
# -------------------------
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
plo2_score = round(df['Complaint_Score'].mean(), 1)
# -------------------------
# PLO 3 – Digital Skill
# Based on number of visualizations used
# -------------------------
num_visualizations = 7  # Heatmap, Pie, Violin, Bar, Stacked Bar, Facet, Metrics
plo3_score = min(round((num_visualizations / 8) * 5, 1), 5)
# -------------------------
# PLO 4 – Interpersonal Skill
# Diversity of complaint behaviour by gender & income
# -------------------------
gender_diversity = df.groupby('Gender')['Complaint_for_Unsuitable_Product'].nunique().mean()
income_diversity = df.groupby('Monthly_Income')['Complaint_for_Unsuitable_Product'].nunique().mean()

plo4_score = round(((gender_diversity + income_diversity) / 2), 1)
# -------------------------
# PLO 5 – Communication Skill
# Based on financial knowledge improvement
# -------------------------
knowledge_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Knowledge_Score'] = df['Increase_Financial_Knowledge'].map(knowledge_mapping)
plo5_score = round(df['Knowledge_Score'].mean(), 1)
# PLO Display
col1.metric(
    label="Calculated from complaint behaviour analysis",
    value=plo2_score,
    help="Calculated from complaint behaviour analysis",
    border=True
)

col2.metric(
    label="Based on number of visualizations implemented",
    value=plo3_score,
    help="Based on number of visualizations implemented",
    border=True
)

col3.metric(
    label="Derived from gender & income complaint diversity",
    value=plo4_score,
    help="Derived from gender & income complaint diversity",
    border=True
)

col4.metric(
    label="Based on increase in financial knowledge",
    value=plo5_score,
    help="Based on increase in financial knowledge",
    border=True
)


#OBJECTIVE AND PROBLEM
st.header("🛒Consumer Rights & Complaint Behaviour")
st.markdown("---")  # this creates a horizontal line

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
# Streamlit section
st.subheader("Complaint Behavior by Monthly Income")
# Create a cross-tabulation (contingency table) of the two categorical variables
contingency_table = pd.crosstab(df['Monthly_Income'], df['Complaint_for_Unsuitable_Product'])
# Define the order for Monthly_Income categories
monthly_income_order = ['Below RM 99', 'RM 100 - RM 500', 'Above RM 600']
contingency_table = contingency_table.reindex(monthly_income_order)
# Normalize the table to show proportions within each 'Monthly_Income' category
contingency_table_normalized = contingency_table.div(contingency_table.sum(1).astype(float), axis=0)
# Plot the stacked bar chart using matplotlib
fig, ax = plt.subplots(figsize=(12, 8))
contingency_table_normalized.plot(kind='bar', stacked=True, colormap='viridis', ax=ax)

ax.set_xlabel('Monthly Income')
ax.set_ylabel('Proportion')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.legend(title='Complaint for Unsuitable Product', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
# Display the plot in Streamlit
st.pyplot(fig)

#Faceted Bar Plot
st.subheader("Financial Knowledge Increase vs Complaint Behaviour")
# Define the order for Increase_Financial_Knowledge categories
financial_knowledge_order = df['Increase_Financial_Knowledge'].value_counts().index.tolist()
# Define the order for Complaint_for_Unsuitable_Product categories
complaint_order = ['Never', 'Sometimes', 'Always']
# Create a faceted bar plot (kind='count')
g = sns.catplot(
    data=df,
    x='Complaint_for_Unsuitable_Product',
    col='Increase_Financial_Knowledge',
    kind='count',
    col_order=financial_knowledge_order,
    order=complaint_order,
    height=5, aspect=1,
    palette='viridis',
    sharey=True,
    hue='Complaint_for_Unsuitable_Product',
    legend=False  # Share the y-axis limit across facets for better comparison
)

g.set_axis_labels('Complaint Behavior', 'Count')
g.set_titles('Financial Knowledge: {col_name}')
plt.suptitle('Complaint Behavior by Financial Knowledge Increase', y=1.05)  # Adjust suptitle position
plt.tight_layout()
# Streamlit: display the plot
st.pyplot(g.fig)
