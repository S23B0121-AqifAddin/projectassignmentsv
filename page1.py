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

# ================== PLO MATRIX (FULL CORRECTION) ==================

# Define PLO → column mapping
plo_mapping = {
    "PLO 2": {
        "label": "Cognitive Skill",
        "columns": [
            "Organised_Money_Management",
            "Plan_for_Old_Age_Care"
        ]
    },
    "PLO 3": {
        "label": "Digital Skill",
        "columns": [
            "Buy_on_Credit",
            "Avoid_Credit_Debt"
        ]
    },
    "PLO 4": {
        "label": "Interpersonal Skill",
        "columns": [
            "Savings_for_Life_Changes",
            "Live_for_Today"
        ]
    },
    "PLO 5": {
        "label": "Communication Skill",
        "columns": [
            "Saver_or_Spender",
            "Follow_Budget"
        ]
    }
}

# (Optional but SAFE) Likert scale mapping
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Replace Likert text with numbers (only where applicable)
data = data.replace(likert_map)

# Calculate PLO scores
plo_scores = {}

for plo, info in plo_mapping.items():

    # Select columns & force numeric conversion
    numeric_data = data[info["columns"]].apply(
        pd.to_numeric, errors="coerce"
    )

    # Mean of columns → mean of respondents
    plo_scores[plo] = round(
        numeric_data.mean(axis=1).mean(),
        2
    )

# ================== DISPLAY PLO METRICS ==================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="PLO 2",
    value=plo_scores["PLO 2"],
    help="PLO 2: Cognitive Skill",
    border=True
)

col2.metric(
    label="PLO 3",
    value=plo_scores["PLO 3"],
    help="PLO 3: Digital Skill",
    border=True
)

col3.metric(
    label="PLO 4",
    value=plo_scores["PLO 4"],
    help="PLO 4: Interpersonal Skill",
    border=True
)

col4.metric(
    label="PLO 5",
    value=plo_scores["PLO 5"],
    help="PLO 5: Communication Skill",
    border=True
)

st.header("Budgeting and spending behavior")
#Objective
st.title("Objective")
st.write("To analyze budgeting and spending behaviour among students and its impact on financial management.")

#Problem statement
st.title("Problem Statement")
st.write(
    """
   Budgeting and spending behaviour play a critical role in financial capability,
   yet many students struggle with effective expense management and financial planning.
   Poor budgeting habits and uncontrolled spending can lead to financial stress and instability.
   Therefore, it is important to examine budgeting and spending behaviour to understand its impact
   on financial decision-making and financial capability.
    """
)

# Tajuk aplikasi
st.title("Correlation Heatmap of Financial Attitudes")
st.write("This heatmap shows the correlation between different financial attitudes of respondents.")

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
st.write("This bar chart to visualize the distribution of Monthly_Income to understand students' income levels.")

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
st.title("Money Management Difficulty by Age Group")
st.write("This grouped bar chart to analyze how 'Money_Management_Difficulty' varies across different 'Age' groups.")

# Plot
fig, ax = plt.subplots(figsize=(12, 7))

sns.countplot(
    x='Age',
    hue='Money_Management_Difficulty',
    data=data,
    palette='viridis',
    ax=ax
)

ax.set_title('Money Management Difficulty by Age Group')
ax.set_xlabel('Age')
ax.set_ylabel('Count')

plt.tight_layout()

# Papar graf dalam Streamlit
st.pyplot(fig)

# Tajuk aplikasi
st.title("Distribution of Gender")
st.write("To visualize the overall distribution of 'Gender' using a pie chart.")

# Kiraan jantina
gender_counts = data['Gender'].value_counts()

# Plot pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('pastel')
)

ax.set_title('Distribution of Gender')
ax.axis('equal')  # Pastikan bulatan sempurna
plt.tight_layout()

# Papar dalam Streamlit
st.pyplot(fig)

# Tajuk aplikasi
st.title("Organised Money Management vs Saver/Spender by Gender")
st.write("This scatter plot to visualize the relationship between 'Organised_Money_Management' and 'Saver_or_Spender', colored by 'Gender'.")

# Plot scatter
fig, ax = plt.subplots(figsize=(10, 6))

sns.scatterplot(
    x='Organised_Money_Management',
    y='Saver_or_Spender',
    hue='Gender',
    data=data,
    palette='viridis',
    ax=ax
)

ax.set_title('Organised Money Management vs. Saver/Spender by Gender')
ax.set_xlabel('Organised Money Management')
ax.set_ylabel('Saver or Spender')

plt.tight_layout()

# Papar graf dalam Streamlit
st.pyplot(fig)

st.subheader("Relationship between Budget Following and Monthly Savings")
st.write("This stacked bar chart to explore the relationship between 'Follow_Budget' and 'Monthly_Savings' to understand budgeting and saving habits.")
fig, ax = plt.subplots(figsize=(10, 6))

# Cross-tabulation
budget_savings_crosstab = pd.crosstab(
    data['Follow_Budget'],
    data['Monthly_Savings'],
    normalize='index'   # untuk proportion
)

budget_savings_crosstab.plot(
    kind='bar',
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
st.pyplot(fig)
