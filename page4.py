import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Consumer Awareness & Information Seeking",
    layout="wide"
)

st.header("Consumer Awareness & Information Seeking", divider="grey")

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv"
df = pd.read_csv(url)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.subheader("Filter Respondents")

gender_options = df["Gender"].dropna().unique()
faculty_options = df["Faculty"].dropna().unique()

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=gender_options,
    default=gender_options
)

selected_faculty = st.sidebar.multiselect(
    "Faculty",
    options=faculty_options,
    default=faculty_options
)

df_filtered = df[
    (df["Gender"].isin(selected_gender)) &
    (df["Faculty"].isin(selected_faculty))
].copy()

# --------------------------------------------------
# CONSUMER AWARENESS VARIABLES
# --------------------------------------------------
awareness_cols = [
    "Search_Info_Before_Buying",
    "Compare_Prices_Before_Buying",
    "Compare_Products_Services",
    "Read_Agreement_Carefully"
]

# --------------------------------------------------
# LIKERT ENCODING (ROBUST)
# --------------------------------------------------
likert_map = {
    "Never": 1,
    "Rarely": 2,
    "Sometimes": 3,
    "Often": 4,
    "Always": 5,
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly agree": 5
}

df_filtered[awareness_cols] = df_filtered[awareness_cols].replace(likert_map)

# FORCE NUMERIC (FIXES TYPEERROR)
df_filtered[awareness_cols] = df_filtered[awareness_cols].apply(
    pd.to_numeric, errors="coerce"
)

# --------------------------------------------------
# COMPOSITE SCORE
# --------------------------------------------------
df_filtered["Consumer_Awareness_Score"] = (
    df_filtered[awareness_cols].mean(axis=1, skipna=True)
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "Average Awareness Score",
    f"{df_filtered['Consumer_Awareness_Score'].mean():.2f} / 5"
)

k2.metric(
    "High Awareness (≥ 4)",
    f"{(df_filtered['Consumer_Awareness_Score'] >= 4).mean() * 100:.1f}%"
)

k3.metric(
    "Number of Respondents",
    df_filtered.shape[0]
)

# --------------------------------------------------
# VISUALIZATION 1: BAR CHART
# --------------------------------------------------
st.subheader("Average Information-Seeking Behaviour")

avg_scores = df_filtered[awareness_cols].mean().reset_index()
avg_scores.columns = ["Behaviour", "Average Score"]

fig1 = px.bar(
    avg_scores,
    x="Behaviour",
    y="Average Score",
    title="Average Scores of Consumer Awareness Behaviours",
    text_auto=".2f"
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "The results indicate that students generally engage in information-seeking behaviours "
    "before making purchases, particularly in comparing prices and searching for information."
)

# --------------------------------------------------
# VISUALIZATION 2: HISTOGRAM
# --------------------------------------------------
st.subheader("Distribution of Consumer Awareness Score")

fig2 = px.histogram(
    df_filtered,
    x="Consumer_Awareness_Score",
    nbins=10,
    title="Distribution of Consumer Awareness Scores"
)

st.plotly_chart(fig2, use_container_width=True)

st.write(
    "Most respondents fall within the moderate to high awareness range, suggesting that "
    "students are somewhat informed consumers but may not consistently apply these behaviours."
)

# --------------------------------------------------
# VISUALIZATION 3: BOX PLOT (AGE)
# --------------------------------------------------
st.subheader("Consumer Awareness Score by Age")

fig3 = px.box(
    df_filtered,
    x="Age",
    y="Consumer_Awareness_Score",
    title="Consumer Awareness Score Across Age Groups"
)

st.plotly_chart(fig3, use_container_width=True)

st.write(
    "A slight increase in consumer awareness is observed among older students, indicating "
    "that experience may contribute to more informed purchasing decisions."
)

# --------------------------------------------------
# VISUALIZATION 4: GROUPED BAR (FACULTY)
# --------------------------------------------------
st.subheader("Consumer Awareness by Faculty")

faculty_avg = (
    df_filtered
    .groupby("Faculty", as_index=False)["Consumer_Awareness_Score"]
    .mean()
)

fig4 = px.bar(
    faculty_avg,
    x="Faculty",
    y="Consumer_Awareness_Score",
    title="Average Consumer Awareness Score by Faculty",
    text_auto=".2f"
)

st.plotly_chart(fig4, use_container_width=True)

st.write(
    "Differences in awareness scores across faculties suggest that academic background may "
    "influence students’ tendency to seek information before making purchasing decisions."
)

# --------------------------------------------------
# VISUALIZATION 5: CORRELATION HEATMAP
# --------------------------------------------------
st.subheader("Correlation Between Consumer Awareness Behaviours")

corr = df_filtered[awareness_cols].corr()

fig5, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap of Consumer Awareness Variables")

st.pyplot(fig5)

st.write(
    "Strong positive correlations indicate that students who actively search for information "
    "also tend to compare prices and read agreements carefully, reflecting consistent "
    "information-seeking behaviour."
)
