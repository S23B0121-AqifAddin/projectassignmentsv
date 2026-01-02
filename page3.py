import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here


# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Financial Behaviour among University Students",
    layout="wide" # Set layout here for consistency
)

# Forced SETUP Page Streamlit
st.markdown(
    """
    <style>
    /* Main reading area */
    .block-container {
        max-width: 900px;          /* Book-like text width */
        padding-top: 3rem;
        padding-bottom: 4rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.8;          /* Comfortable reading */
    }

    /* Improve text readability */
    p, li {
        font-size: 1.05rem;
    }

    h1, h2, h3 {
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }

    .stApp {
        /* Overlay a semi-transparent black on the image */
    background-image: 
        linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
        url("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# DATASET UPLOAD AND SUMMARY BOX
# Page header
st.title("💷Financial Behaviour among University Students(KHADIJAH)")
st.markdown("---")  # this creates a horizontal line
# Summary Box
col1, col2, col3, col4 = st.columns(4)

# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Khadijah)%20processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Khadijah)%20processed_financial_capability_data.csv', encoding='latin-1')
df

# =========================
# PLO DATA CALCULATIONS
# =========================

total_students = len(df)
# -------------------------
# PLO 1 – Cognitive Skill
# Complaint awareness level
# -------------------------
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
plo1_score = round(df['Complaint_Score'].mean(), 1)
# -------------------------
# -------------------------
# PLO 2 – Digital Skill
# Age × Complaint Behaviour
# -------------------------
# Convert Age to numeric (safety)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
# Map complaint behaviour to numeric values
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
# Calculate mean complaint score by age group
age_complaint_score = (
    df.dropna(subset=['Age', 'Complaint_Score'])
      .groupby('Age')['Complaint_Score']
      .mean()
)
# Final PLO 2 score
plo2_score = round(age_complaint_score.mean(), 1)
# -------------------------
# PLO 3 – Interpersonal Skill
# Financial Knowledge × Complaint Behaviour
# -------------------------
# Map complaint behaviour to numeric values
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
# Calculate mean complaint score by financial knowledge level
knowledge_complaint_score = (
    df.dropna(subset=['Increase_Financial_Knowledge', 'Complaint_Score'])
      .groupby('Increase_Financial_Knowledge')['Complaint_Score']
      .mean()
)
# Final PLO 3 score
plo3_score = round(knowledge_complaint_score.mean(), 1)
# -------------------------
# PLO 4 – Interpersonal Skill
# Complaint Behaviour by Monthly Income
# -------------------------
# Ensure Monthly Income is treated as string
# Map complaint behaviour to numeric values
complaint_mapping = {
    'Never': 1,
    'Sometimes': 3,
    'Always': 5
}

df['Complaint_Score'] = df['Complaint_for_Unsuitable_Product'].map(complaint_mapping)
# Calculate mean complaint score by monthly income group
income_complaint_score = (
    df.dropna(subset=['Monthly_Income', 'Complaint_Score'])
      .groupby('Monthly_Income')['Complaint_Score']
      .mean()
)
# Final PLO 4 score
plo4_score = round(income_complaint_score.mean(), 1)
# PLO Display
col1.metric(
    label="Complaint Behaviour",
    value=plo1_score,
    help="Calculated from complaint behaviour analysis",
    border=True
)

col2.metric(
    label="Age and Complaint",
    value=plo2_score,
    help="Calculated from digital analysis of Age and Complaint Behaviour",
    border=True
)

col3.metric(
    label="Complaint by Knowledge",
    value=plo3_score,
    help="Calculated from analysis of complaint behaviour across financial knowledge levels",
    border=True
)

col4.metric(
    label="Complaint by Income",
    value=plo4_score,
    help="Based on complaint behaviour across monthly income groups",
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
#Distribution Demographic Graph
st.subheader("Demographic of Students")
st.write(
    "This section provides an overview of the students' demographics, "
    "including age, gender, faculty, housing arrangement, main income source and monthly income. "
    "Use the selector below to choose which demographic graph to display."
)
# Main page container
with st.container():
    # Selector INSIDE the page
    chart_option = st.selectbox(
        "List of Graph:",
        (
            "Age Distribution",
            "Gender Distribution",
            "Faculty Distribution",
            "Housing Arrangement Distribution",
            "Main Income Source Distribution",
            "Monthly Income Distribution"
        )
    )
    # 1. Age Distribution
    if chart_option == "Age Distribution":
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df['Age'], kde=True, ax=ax)
        ax.set_title("Distribution of Age")
        ax.set_xlabel("Age")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    # 2. Gender Distribution
    elif chart_option == "Gender Distribution":
        fig, ax = plt.subplots(figsize=(8, 6))
        gender_counts = df['Gender'].value_counts()
        ax.pie(
            gender_counts,
            labels=gender_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette('pastel')
        )
        ax.set_title("Distribution of Gender")
        ax.axis("equal")
        st.pyplot(fig)
    # 3. Faculty Distribution
    elif chart_option == "Faculty Distribution":
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(
            y=df['Faculty'],
            order=df['Faculty'].value_counts().index,
            hue=df['Faculty'],
            palette='viridis',
            legend=False,
            ax=ax
        )
        ax.set_title("Distribution of Faculty")
        ax.set_xlabel("Count")
        ax.set_ylabel("Faculty")
        st.pyplot(fig)
    # 4. Housing Arrangement Distribution
    elif chart_option == "Housing Arrangement Distribution":
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(
            y=df['Housing_Arrangement'],
            order=df['Housing_Arrangement'].value_counts().index,
            hue=df['Housing_Arrangement'],
            palette='coolwarm',
            legend=False,
            ax=ax
        )
        ax.set_title("Distribution of Housing Arrangement")
        ax.set_xlabel("Count")
        ax.set_ylabel("Housing Arrangement")
        st.pyplot(fig)
    # 5. Main Income Source Distribution
    elif chart_option == "Main Income Source Distribution":
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(
            y=df['Main_Income_Source'],
            order=df['Main_Income_Source'].value_counts().index,
            hue=df['Main_Income_Source'],
            palette='plasma',
            legend=False,
            ax=ax
        )
        ax.set_title("Distribution of Main Income Source")
        ax.set_xlabel("Count")
        ax.set_ylabel("Main Income Source")
        st.pyplot(fig)
    # 6. Monthly Income Distribution
    elif chart_option == "Monthly Income Distribution":
        monthly_income_order = [
            'Below RM 99',
            'RM 100 - RM 500',
            'Above RM 600'
        ]

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(
            y=df['Monthly_Income'],
            order=monthly_income_order,
            hue=df['Monthly_Income'],
            palette='magma',
            legend=False,
            ax=ax
        )
        ax.set_title("Distribution of Monthly Income")
        ax.set_xlabel("Count")
        ax.set_ylabel("Monthly Income")
        st.pyplot(fig)
st.markdown("---")  # this creates a horizontal line

#Heatmap
st.subheader("Correlation of Financial Management and Planning Behaviours")
st.write(
    "This heatmap illustrates the strength and direction of relationships among financial "
    "management and planning behaviours. Strong positive correlations suggest behaviours "
    "that tend to occur together, while negative correlations indicate contrasting habits."
)
# Select the numerical columns related to financial management and planning behaviors
selected_numerical_cols = [
    'Age',
    'Organised_Money_Management',
    'More_of_a_Saver_Than_a_Spender',
    'Prefer_to_Buy_on_Credit',
    'Savings_for_Rainy_Day',
    'Prefer_to_Live_for_Today',
]
# Calculate the correlation matrix
correlation_matrix = df[selected_numerical_cols].corr()
# Create the matplotlib figure
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    linewidths=0.5,
    ax=ax
)

ax.set_title("Correlation Heatmap of Financial Management and Planning Behaviors")
# Display the plot inside Streamlit
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
st.write(
    "This stacked bar chart shows the proportion of students who file complaints about unsuitable products, "
    "segmented by their monthly income. Each bar represents a different income group, "
    "and the colors indicate the frequency of complaint behaviour (Never, Sometimes, Always). "
    "It helps to identify if income level influences students' likelihood to submit complaints."
)
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
st.write(
    "This faceted bar compares complaint behaviour across different levels of financial knowledge increase. "
    "Each faceted bar represents a level of financial knowledge, showing how student's complaint patterns. "
    "It helps to evaluate whether higher financial knowledge influences students to submit complaints more frequently."
)
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
