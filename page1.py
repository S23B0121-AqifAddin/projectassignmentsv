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
st.header("Financial Behaviour among University Students(AISYAH)", divider="grey")

col1, col2, col3, col4 = st.columns(4)

# Load your data
try:
    data = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Aisyah)%20financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Aisyah)%20financial_capability_data.csv', encoding='latin-1')
data

# ================== SAFE PLO MATRIX (FINAL) ==================

# Define PLO → column mapping
plo_mapping = {
    "PLO 2": {
        "label": "Money Management",
        "columns": [
            "Organised_Money_Management",
            "Plan_for_Old_Age_Care"
        ]
    },
    "PLO 3": {
        "label": "Buy on Credit",
        "columns": [
            "Buy_on_Credit",
            "Avoid_Credit_Debt"
        ]
    },
    "PLO 4": {
        "label": "Saving Life Changes",
        "columns": [
            "Savings_for_Life_Changes",
            "Live_for_Today"
        ]
    },
    "PLO 5": {
        "label": "Saver or Spender",
        "columns": [
            "Saver_or_Spender",
            "Follow_Budget"
        ]
    }
}

# Likert scale mapping (safe even if not used)
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Replace Likert text → numbers
data = data.replace(likert_map)

# Calculate PLO scores safely
plo_scores = {}

for plo, info in plo_mapping.items():
    numeric_data = (
        data[info["columns"]]
        .apply(pd.to_numeric, errors="coerce")
        .astype(float)
    )

    plo_scores[plo] = round(
        numeric_data.stack().mean(),  # ✅ safest mean method
        2
    )

# ================== DISPLAY ==================

col1.metric("Money Management", plo_scores["PLO 2"], help="Money Management", border=True)
col2.metric("Buy on Credit", plo_scores["PLO 3"], help="Buy on Credit", border=True)
col3.metric("Saving Life Changes", plo_scores["PLO 4"], help="Saving Life Changes", border=True)
col4.metric("Saver or Spender", plo_scores["PLO 5"], help="Saver or Spender", border=True)


st.header("Budgeting and Spending Behavior")
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
st.write("""
This heatmap shows the correlation between different financial attitudes of respondents such as organised money management,
saving for emergencies, retirement, and future life changes are strongly related to each other, indicating that students who plan well 
financially tend to practice multiple good financial habits. In contrast, buying on credit and a “live for today” attitude show weak or 
negative relationships with saving and long-term planning, suggesting these behaviours are largely independent of responsible financial management.
""")

# Load dataset dari GitHub
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Aisyah)%20financial_capability_data.csv"
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
st.write("""
This bar chart show the distribution of Monthly_Income to understand students' income levels, 
where most respondents fall within the RM 100–RM 500 range, indicating this is the most common income level. 
In comparison, fewer students earn below RM 99 or above RM 600, suggesting that very low and relatively higher
monthly incomes are less common among the respondents.
""")

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
st.write("""
This grouped bar chart to analyze how 'Money_Management_Difficulty' varies across different 'Age' groups, 
indicating that most students around age 21 report having some difficulty managing their money, followed by those who always experience difficulty, 
while fewer report never having issues. In contrast, younger (age 18) and older (age 26) students appear in much smaller numbers, 
suggesting that money management challenges are most common among students in the main university age group.
""")

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
st.write("""
This visualize the overall distribution of 'Gender' using a pie chart 
shows a significant majority of Females at 73.5% compared to Males at 26.5%.
""")

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
st.write("""
This scatter plot show the relationship between 'Organised_Money_Management' and 'Saver_or_Spender', colored by 'Gender'. 
The graph displays data points for both females (blue) and males (green) across two five-point scales. Notably, 
the female data points are more widely distributed across the entire grid, appearing at almost every intersection of the scales from 1 to 5. 
In contrast, the male data points are much more sparse, appearing primarily at specific intersections such as (2, 2), (3, 2), and (4, 4). 
This suggests that in this specific dataset, females exhibit a broader range of financial behaviors, while the male sample is smaller and more clustered.
""")

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
st.write("""
This stacked bar chart to explore the relationship between 'Follow_Budget' and 'Monthly_Savings' to understand budgeting and saving habits students
who always follow a budget are the most successful savers, with approximately 75% of them managing to save every month. 
Conversely, those who never follow a budget face the most difficulty, as roughly 30% of that group never saves and less than 10% save consistently, 
Sometimes Follow Budget the majority of these students (about 65%) manage to save.
""")
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


st.write("""
Click a section below to view another page.
""")

col1, col2, = st.columns(2)

with col1:
    if st.button("🧠 Aqif – Financial Decision-Making", use_container_width=True):
        st.switch_page("page2.py")
        
    if st.button("🔍 Kisantini – Consumer Awareness", use_container_width=True):
        st.switch_page("page4.py")

with col2:
    if st.button("🧾 Khadijah – Consumer Rights", use_container_width=True):
        st.switch_page("page3.py")
        
    if st.button("👥 Group Overview", use_container_width=True):  # New button
        st.switch_page("homepage.py")  # Replace with your homepage file
