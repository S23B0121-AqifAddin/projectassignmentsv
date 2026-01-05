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

    p {
        text-align: justify;
    }
    
    .stMarkdown p {
    background-color: #EEE6FF;   /* color box */
    border: 2.0px solid #888888; /* color border */
    color: #000000;              /* color text */
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    text-align: justify;
    margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# DATASET UPLOAD AND SUMMARY BOX
# Page header
st.title("💷Financial Behaviour among University Students")
st.markdown("---")  # this creates a horizontal line
# Summary Box
col1, col2, col3, col4 = st.columns(4)

# Load your data
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Khadijah)%20processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/(Khadijah)%20processed_financial_capability_data.csv', encoding='latin-1')
df
# Display row × column info
st.markdown(f"<div style='font-size:12px; color:gray; margin:0; padding:0;'>Rows: {df.shape[0]} × Columns: {df.shape[1]}</div>", unsafe_allow_html=True)

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
        st.write(
            """
            The "Distribution of Age" graph shows a histogram with an overlay of a kernel density estimate (KDE) curve. 
            The largest bar and the strong peak in the KDE curve at age 21 show that most students in the study are 21. At ages 18 and 26, 
            there are quite fewer students, and the frequency of students declines on each side of age 21. The KDE curve highlights 
            the overall layout of the data and underlines the peak around age 21 by offering a smooth simulation of the age distribution. 
            The dataset appears to have a significant overall pattern, with age 21 being the most typical population, 
            according to this visualisation.
            """
        )
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df['Age'], kde=True, ax=ax)
        ax.set_title("Distribution of Age")
        ax.set_xlabel("Age")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    # 2. Gender Distribution
    elif chart_option == "Gender Distribution":
        st.write(
            """
            The "Distribution of Gender" pie chart shows the percentage of men and women in a dataset. It shows that 26.5% are men (shown in orange), 
            while 73.5% are women (shown in light blue). Having over three times as many women's students as men in this university student, this suggests a severe gender imbalance. 
            For an overview of demographic characteristics, the chart offers a clear visual summary of gender ratio.
            """
        )
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
        st.write(
            """
           The number of people in each faculty is displayed as a horizontal bar graph in the "Distribution of Faculty" chart. 
           With more than 60 students, FSDK is the faculty with the largest presence. The "Other" group, which includes about thirty people, 
           comes next. With counts of less than 20, the other faculties is FKP, FHPK, FBI, FBKT, FSB, and FIAT, have a fewer students. 
           This distribution shows a lowest appearance in the other faculties and an impressive majority in FSDK.
            """
        )
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
        st.write(
            """
           The "Distribution of Housing Arrangement" graphic shows how student are categorised according to their living situations. 
           Off-campus rent (sharing a house or flat) with more than fifty students is the most in this typical option. The numbers for living on 
           campus and with parents or other family members are equivalent, ranging from 21 to 22. Off-campus (own) living is the least usual arrangement, 
           with just around five students. This means living independently off campus is more uncommon, whereas shared off-campus accommodation is the favoured option.
            """
        )
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
        st.write(
            """
            The "Distribution of Main Income Source" visualisation shows how student have support financially. 
            The majority, almost 70 students depend on their parent's pocket money as their main source of income. 
            Another 15 students are supported by scholarships, while another 10 are supported by other means. 
            Only around two of the smaller group and roughly seven students is depend on other family members for their income and part-time work. 
            This distribution shows a considerable dependency on parental support, while very few students earning money on their own or earning scholarships.
            """
        )
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
        st.write(
            """
            The "Distribution of Monthly Income" figure shows how students are divided into three income groups. 
            The majority fall between RM 100 and RM 500, suggesting that this is the most typical monthly income range. 
            A lower percentage of students make less than RM 99, while an even smaller percentage make more than RM 600. 
            This means that the majority of students in this study have moderate monthly incomes, with just a few at the higher and lower ends of the income range.
            """
        )
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


viz_option = st.radio(
    "Select a visualization",
    [
        "Correlation Heatmap",
        "Complaint Behaviour (Pie Chart)",
        "Age vs Complaint (Violin Plot)",
        "Complaint by Gender (Grouped Bar)",
        "Complaint by Monthly Income (Stacked Bar)",
        "Financial Knowledge vs Complaint (Faceted Bar)"
    ],
    horizontal=True
)

# ============================
# 1️⃣ CORRELATION HEATMAP
# ============================
if viz_option == "Correlation Heatmap":
    st.subheader("Correlation of Financial Management and Planning Behaviours")
    st.write("""
     The "Correlation Heatmap of Financial Management and Planning Behaviours" illustrates the relationships between financial behaviours. 
    Organised money management, saving for a rainy day (0.67), and being more of a saver than a spender (0.71) all show strong positive relationships. 
    Additionally, there is a moderate correlation (0.45) between saving for a rainy day and being a saver. On the other hand, behaviours such as living in the now or 
    preferring credit purchases indicate weaker or unfavourable connections. Overall, the heatmap shows how saving habits and organised money management typically support one another.
    """)

    selected_numerical_cols = [
        'Age',
        'Organised_Money_Management',
        'More_of_a_Saver_Than_a_Spender',
        'Prefer_to_Buy_on_Credit',
        'Savings_for_Rainy_Day',
        'Prefer_to_Live_for_Today',
    ]

    corr = df[selected_numerical_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        title="Correlation Heatmap of Financial Behaviours"
    )

    fig.update_layout(
    height=600,   # ↓ smaller than default
    width=700,    # optional (Streamlit usually auto-scales)
    margin=dict(t=60, b=40, l=40, r=40)
    )


    st.plotly_chart(fig, use_container_width=True)
# ============================
# 2️⃣ PIE CHART
# ============================
elif viz_option == "Complaint Behaviour (Pie Chart)":
    st.subheader("Complaint Behavior for Unsuitable Products")
    st.write("""
   The "Distribution of Complaint Behaviour for Unsuitable Products" pie chart has shows how students react when they come with unacceptable products. 
    Those who frequently complain make up the biggest population (41.2%), followed closely by those who complain occasionally (39.2%). 
    Just 19.6% of people never complain. This implies that the majority of people actively express their dissatisfaction, with only a small percentage choosing to do nothing.
    """)

    complaint_counts = df['Complaint_for_Unsuitable_Product'].value_counts().reset_index()
    complaint_counts.columns = ['Behaviour', 'Count']

    fig = px.pie(
        complaint_counts,
        names='Behaviour',
        values='Count',
        title='Distribution of Complaint Behaviour'
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}"
    )

    fig.update_layout(
    height=500,   # ↓ smaller than default
    width=700,    # optional (Streamlit usually auto-scales)
    margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig, use_container_width=True)
# ============================
# 3️⃣ VIOLIN PLOT
# ============================
elif viz_option == "Age vs Complaint (Violin Plot)":
    st.subheader("Age Distribution and Complaint Behaviour")
    st.write("""
    The *Age Distribution by Complaint Behaviour* violin plot illustrates the variation 
    in age across different complaint categories. Wider distributions among students who 
    complain sometimes or always indicate greater age diversity, whereas the narrow 
    distribution among those who never complain suggests limited age variation. The 
    median age in each category further highlights differences in complaint tendencies 
    across age groups.
    """)
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
# ============================
# 4️⃣ GROUPED BAR
# ============================
elif viz_option == "Complaint by Gender (Grouped Bar)":
    st.subheader("Complaint Behaviour by Gender")
    st.write("""
    The "Complaint Behaviour by Gender" visualisation shows how men's student and women's student react to inappropriate items in three different complaint categories 
    which is Always, Sometimes, and Never. Complaints are more common among student by women, with "Always" accounting for the largest percentage, followed by "Sometimes". 
    Although they are less common than females, men's students also fall into the "Always" and "Sometimes" categories. unexpectedly, the "Never" group only includes females, 
    suggesting that every guy in the dataset expresses a sense of dissatisfaction. This implies that while men's students usually express a sense of unhappiness, women's students 
    have a greater variety of complaint behaviours.
    """)

    fig = px.histogram(
        df,
        x='Complaint_for_Unsuitable_Product',
        color='Gender',
        barmode='group',
        title='Complaint Behaviour by Gender'
    )

    fig.update_layout(
    height=550,   # ↓ smaller than default
    width=700,    # optional (Streamlit usually auto-scales)
    margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig, use_container_width=True)
# ============================
# 5️⃣ STACKED BAR
# ============================
elif viz_option == "Complaint by Monthly Income (Stacked Bar)":
    st.subheader("Complaint Behaviour by Monthly Income")
    st.write("""
    The "Complaint Behaviour by Monthly Income" illustration has shows how student in different income categories react to inappropriate products. 
    Most students in all three income groups is below RM 99, between RM 100 and RM 500, and above RM 600, either often or sometimes complain. The "Never" 
    category is always the smallest, suggesting that relatively few students decide not to express their dissatisfaction. "Always" and "Sometimes" 
    are distributed fairly evenly in the RM 100–RM 500 category, although "Always" is more common in the other two categories. Given that most people voice 
    complaints no matter their financial status, this shows that income level does not considerably prevent complaint behaviour.
    """)

    fig = px.histogram(
        df,
        x='Monthly_Income',
        color='Complaint_for_Unsuitable_Product',
        barnorm='percent',
        title='Complaint Behaviour by Monthly Income'
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{legendgroup}<br>Percentage: %{y:.1f}%"
    )

    fig.update_layout(
    height=550,   # ↓ smaller than default
    width=700,    # optional (Streamlit usually auto-scales)
    margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig, use_container_width=True)
# ============================
# 6️⃣ FACETED BAR
# ============================
elif viz_option == "Financial Knowledge vs Complaint (Faceted Bar)":
    st.subheader("Financial Knowledge Increase vs Complaint Behaviour")
    st.write("""
     The "Complaint Behaviour by Financial Knowledge Increase" visualisation has illustrates how student's complaint behaviour changes 
    according to their level of financial understanding. "Sometimes" is the most frequent complaint behaviour among people who say their financial 
    understanding sometimes improves, followed by "Always" and "Never". Most people who are always learning more about finance always complain, while a 
    smaller percentage choose to complain is sometimes or never. On the other hand, those whose financial literacy never improves are more likely to never 
    complain, and very few of them actually do. This trend shows a relationship between consumer confidence and financial awareness, those who are more 
    knowledgeable about finances are more likely to express their disapproval.
    """)

    fig = px.histogram(
        df,
        x='Complaint_for_Unsuitable_Product',
        facet_col='Increase_Financial_Knowledge',
        color='Complaint_for_Unsuitable_Product',
        title='Complaint Behaviour by Financial Knowledge Increase'
    )

    fig.update_layout(
    height=550,   # ↓ smaller than default
    width=700,    # optional (Streamlit usually auto-scales)
    margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.markdown("""
<style>
.no-box {
    color: var(--text-color) !important;
    background: none !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}
.center-only {
    text-align: center !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
<p class="no-box">Click a section below to view another page.</p>
""", unsafe_allow_html=True)

# Centered instruction text (no box, no gap)
st.markdown(
    "<p class='center-only'>Click a section below to view another page.</p>",
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Kisantini – Consumer Awareness", use_container_width=True):
        st.switch_page("page4.py")

    if st.button("🧠 Aqif – Financial Decision-Making", use_container_width=True):
        st.switch_page("page2.py")

with col2:
    if st.button("📊 Aisyah – Budgeting & Spending Behaviour", use_container_width=True):
        st.switch_page("page1.py")

    if st.button("👥 Group Overview", use_container_width=True):  # New button
        st.switch_page("homepage.py")  # Replace with your homepage file       
