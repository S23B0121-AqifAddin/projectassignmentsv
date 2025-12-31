import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. SETTING PREFERENCE
st.set_page_config(
    page_title="💷 Financial Behaviour among University Students",
    layout="wide"
)

# Page header
st.title("💷 Financial Behaviour among University Students")
st.markdown("---")

# 2. DATASET UPLOAD
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv'
    try:
        return pd.read_csv(url, encoding='utf-8')
    except:
        return pd.read_csv(url, encoding='latin-1')

df = load_data()

# 3. PLO DATA CALCULATIONS (Financial Responsibility & Decision-Making)
# We use 'Complaint_for_Unsuitable_Product' as a proxy for Financial Responsibility
responsibility_mapping = {'Never': 1, 'Sometimes': 3, 'Always': 5}
df['Responsibility_Score'] = df['Complaint_for_Unsuitable_Product'].map(responsibility_mapping)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Metric 1: Overall Index
plo1_score = round(df['Responsibility_Score'].mean(), 1)
# Metric 2: Maturity by Age
plo2_score = round(df.dropna(subset=['Age', 'Responsibility_Score']).groupby('Age')['Responsibility_Score'].mean().mean(), 1)
# Metric 3: Knowledge Impact
plo3_score = round(df.dropna(subset=['Increase_Financial_Knowledge', 'Responsibility_Score']).groupby('Increase_Financial_Knowledge')['Responsibility_Score'].mean().mean(), 1)
# Metric 4: Economic Capability
plo4_score = round(df.dropna(subset=['Monthly_Income', 'Responsibility_Score']).groupby('Monthly_Income')['Responsibility_Score'].mean().mean(), 1)

# 4. SUMMARY METRICS BOX
# Defining these immediately before use prevents NameErrors
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

m_col1.metric(label="Financial Responsibility Index", value=plo1_score, border=True, help="Proactive consumer behavior score.")
m_col2.metric(label="Decision Maturity (Age)", value=plo2_score, border=True, help="Responsibility levels across age groups.")
m_col3.metric(label="Knowledge-Driven Actions", value=plo3_score, border=True, help="How knowledge influences decisions.")
m_col4.metric(label="Economic Decision Power", value=plo4_score, border=True, help="Responsibility based on income brackets.")

# 5. OBJECTIVE AND PROBLEM
st.header("🛒 Consumer Rights & Complaint Behaviour")
st.markdown("---")

st.subheader("Objective")
st.write("Study about student's awareness of consumer rights and their complaint behaviour after purchasing products.")

st.subheader("Problem Definition")
st.write("Many students might not be aware of their rights. Dissatisfaction with products may not lead to formal complaints. Does knowledge equate to action?")

# 6. VISUALIZATIONS
st.subheader("Demographic of Students")
chart_option = st.selectbox(
    "List of Graph:",
    ("Age Distribution", "Gender Distribution", "Faculty Distribution", "Monthly Income Distribution")
)

if chart_option == "Age Distribution":
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df['Age'], kde=True, ax=ax, color='teal')
    ax.set_title("Age Distribution of Respondents")
    st.pyplot(fig)

elif chart_option == "Gender Distribution":
    fig, ax = plt.subplots(figsize=(6, 6))
    gender_counts = df['Gender'].value_counts()
    ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
    st.pyplot(fig)

st.markdown("---")

# 7. CORRELATION ANALYSIS
st.subheader("Correlation of Financial Management and Planning Behaviours")

selected_numerical_cols = [
    'Organised_Money_Management', 'Saver_or_Spender', 'Buy_on_Credit',
    'Avoid_Credit_Debt', 'Savings_for_Rainy_Day', 'Pension_Funds_for_Retirement',
    'Live_for_Today', 'Savings_for_Life_Changes', 'Plan_for_Old_Age_Care'
]
correlation_matrix = df[selected_numerical_cols].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)

# 8. BEHAVIORAL ANALYSIS
st.subheader("Age Distribution and Complaint Behaviour")

fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(x='Complaint_for_Unsuitable_Product', y='Age', data=df, hue='Complaint_for_Unsuitable_Product', palette='viridis', ax=ax)
st.pyplot(fig)
