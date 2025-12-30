import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. SETTING PREFERENCE
st.set_page_config(
    page_title="💷 Financial Behaviour Dashboard",
    layout="wide"
)

# Page header
st.title("💷 Financial Behaviour among University Students")
st.markdown("---")

# 2. DATASET LOADING
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv'
    try:
        data = pd.read_csv(url, encoding='utf-8')
    except:
        data = pd.read_csv(url, encoding='latin-1')
    return data

df = load_data()

# 3. CALCULATIONS (Financial Responsibility & Decision-Making)
responsibility_mapping = {'Never': 1, 'Sometimes': 3, 'Always': 5}
df['Responsibility_Score'] = df['Complaint_for_Unsuitable_Product'].map(responsibility_mapping)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Metric Values
plo1 = round(df['Responsibility_Score'].mean(), 1)
plo2 = round(df.dropna(subset=['Age', 'Responsibility_Score']).groupby('Age')['Responsibility_Score'].mean().mean(), 1)
plo3 = round(df.dropna(subset=['Increase_Financial_Knowledge', 'Responsibility_Score']).groupby('Increase_Financial_Knowledge')['Responsibility_Score'].mean().mean(), 1)
plo4 = round(df.dropna(subset=['Monthly_Income', 'Responsibility_Score']).groupby('Monthly_Income')['Responsibility_Score'].mean().mean(), 1)

# 4. TOP METRICS ROW
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Financial Responsibility Index", plo1, help="Overall average responsibility score.", border=True)
m_col2.metric("Decision Maturity (Age)", plo2, help="Responsibility score normalized by age.", border=True)
m_col3.metric("Knowledge-Driven Actions", plo3, help="Impact of financial knowledge on behavior.", border=True)
m_col4.metric("Economic Decision Power", plo4, help="Responsibility levels across income brackets.", border=True)

st.markdown("---")

# 5. TABBED VISUALIZATION SECTION
st.subheader("Data Analysis & Exploration")

# Creating the Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Student Demographics", 
    "📈 Correlation Analysis", 
    "🛡️ Consumer Rights", 
    "💰 Income & Knowledge"
])

# --- TAB 1: DEMOGRAPHICS ---
with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Age Distribution**")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.histplot(df['Age'], kde=True, color='skyblue', ax=ax1)
        st.pyplot(fig1)
    
    with col_b:
        st.write("**Gender Distribution**")
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        gender_counts = df['Gender'].value_counts()
        ax2.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        st.pyplot(fig2)

# --- TAB 2: CORRELATION ---
with tab2:
    st.write("**Financial Planning Relationships**")
    

[Image of a correlation matrix heatmap]

    selected_cols = [
        'Organised_Money_Management', 'Saver_or_Spender', 'Buy_on_Credit',
        'Avoid_Credit_Debt', 'Savings_for_Rainy_Day', 'Pension_Funds_for_Retirement'
    ]
    corr = df[selected_cols].corr()
    fig3, ax3 = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
    st.pyplot(fig3)

# --- TAB 3: CONSUMER RIGHTS ---
with tab3:
    st.write("**Complaint Behavior by Age (Violin Plot)**")
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.violinplot(x='Complaint_for_Unsuitable_Product', y='Age', data=df, palette='muted', ax=ax4)
    st.pyplot(fig4)

# --- TAB 4: INCOME & KNOWLEDGE ---
with tab4:
    col_c, col_d = st.columns(2)
    with col_c:
        st.write("**Knowledge vs Complaint**")
        fig5 = sns.catplot(data=df, x='Complaint_for_Unsuitable_Product', col='Increase_Financial_Knowledge', kind='count', height=4, aspect=0.8, palette='viridis')
        st.pyplot(fig5.fig)
    
    with col_d:
        st.write("**Income Level Proportions**")
        income_order = ['Below RM 99', 'RM 100 - RM 500', 'Above RM 600']
        ct = pd.crosstab(df['Monthly_Income'], df['Complaint_for_Unsuitable_Product']).reindex(income_order)
        ct_norm = ct.div(ct.sum(1), axis=0)
        fig6, ax6 = plt.subplots()
        ct_norm.plot(kind='bar', stacked=True, ax=ax6, colormap='viridis')
        st.pyplot(fig6)

# 6. OBJECTIVES (Placed at the bottom for a cleaner look)
with st.expander("View Project Objectives & Problem Definition"):
    st.write("**Objective:** To analyze awareness of consumer rights among students.")
    st.write("**Problem:** Dissatisfaction often doesn't lead to formal complaints; is this due to lack of knowledge?")
