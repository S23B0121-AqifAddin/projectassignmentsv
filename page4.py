import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Consumer Awareness & Information Seeking",
    layout="wide"
)

st.header("Consumer Awareness & Information Seeking", divider="grey")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv"
df = pd.read_csv(url)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.subheader("Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].dropna().unique(),
    default=df["Gender"].dropna().unique()
)

faculty_filter = st.sidebar.multiselect(
    "Select Faculty",
    options=df["Faculty"].dropna().unique(),
    default=df["Faculty"].dropna().unique()
)

df_filtered = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Faculty"].isin(faculty_filter))
]

# --------------------------------------------------
# Likert Encoding
# --------------------------------------------------
likert_map = {
    "Never": 1,
    "Rarely": 2,
    "Sometimes": 3,
    "Often": 4,
    "Always": 5
}

awareness_cols = [
    "Search_Info_Before_Buying",
    "Compare_Prices_Before_Buying",
    "Compare_Products_Services",
    "Read_Agreement_Carefully"
]

df_filtered[awareness_cols] = df_filtered[awareness_cols].replace(likert_map)

# --------------------------------------------------
# Composite Score
# --------------------------------------------------
df_filtered["Consumer_Awareness_Score"] = df_filtered[awareness_cols].mean(axis=1)

# --------------------------------------------------
# KPI Section
# --------------------------------------------------
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "Average Awareness Score",
    f"{df_filtered['Consumer_Awareness_Score'].mean():.2f} / 5"
)

kpi2.metric(
    "High Awareness (%)",
    f"{(df_filtered['Consumer_Awareness_Score'] >= 4).mean() * 100:.1f}%"
)

kpi3.metric(
    "Sample Size",
    df_filtered.shape[0]
)

# --------------------------------------------------
# Visualization 1: Bar Chart
# --------------------------------------------------
st.subheader("Information-Seeking Behaviour Frequency")

fig1 = px.bar(
    df_filtered[awareness_cols].mean().reset_index(),
    x="index",
    y=0,
    labels={"index": "Behaviour", "0": "Average Score"},
    title="Average Scores of Information-Seeking Behaviours"
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "Students generally report moderate to high levels of information-seeking behaviour, "
    "with price comparison and information search being the most common practices."
)

# --------------------------------------------------
# Visualization 2: Histogram
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
    "The distribution shows that most students fall within the mid-to-high awareness range, "
    "suggesting partial but not consistent proactive consumer behaviour."
)

# --------------------------------------------------
# Visualization 3: Box Plot (Age)
# --------------------------------------------------
st.subheader("Consumer Awareness by Age")

fig3 = px.box(
    df_filtered,
    x="Age",
    y="Consumer_Awareness_Score",
    title="Consumer Awareness Score Across Age Groups"
)

st.plotly_chart(fig3, use_container_width=True)

st.write(
    "Older students tend to exhibit slightly higher awareness scores, indicating experience "
    "may play a role in informed purchasing decisions."
)

# --------------------------------------------------
# Visualization 4: Grouped Bar (Faculty)
# --------------------------------------------------
st.subheader("Consumer Awareness by Faculty")

faculty_mean = (
    df_filtered
    .groupby("Faculty")["Consumer_Awareness_Score"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    faculty_mean,
    x="Faculty",
    y="Consumer_Awareness_Score",
    title="Average Consumer Awareness Score by Faculty"
)

st.plotly_chart(fig4, use_container_width=True)

st.write(
    "Differences across faculties suggest varying exposure to consumer-related knowledge, "
    "with some academic backgrounds encouraging more informed decision-making."
)

# --------------------------------------------------
# Visualization 5: Correlation Heatmap
# --------------------------------------------------
st.subheader("Correlation Between Awareness Behaviours")

corr = df_filtered[awareness_cols].corr()

fig5, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap of Consumer Awareness Variables")

st.pyplot(fig5)

st.write(
    "Strong positive correlations indicate that students who actively search for information "
    "are also more likely to compare alternatives and read agreements carefully."
)
