import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Consumer Awareness & Information Seeking",
    layout="wide"
)

st.header("Consumer Awareness & Information Seeking", divider="grey")

st.write(
    """
    This section examines how proactive university students are in seeking
    information before making purchasing decisions, including comparing prices,
    reading agreements, and searching for product information.
    """
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv"
df = pd.read_csv(url)

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

# Replace and FORCE numeric conversion (CRITICAL FIX)
df[awareness_cols] = (
    df[awareness_cols]
    .replace(likert_map)
    .apply(pd.to_numeric, errors="coerce")
)

# --------------------------------------------------
# Composite Score
# --------------------------------------------------
df["Consumer_Awareness_Score"] = df[awareness_cols].mean(axis=1, skipna=True)

# --------------------------------------------------
# KPI Section
# --------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "Average Awareness Score",
    f"{df['Consumer_Awareness_Score'].mean():.2f} / 5"
)

k2.metric(
    "High Awareness (%)",
    f"{(df['Consumer_Awareness_Score'] >= 4).mean() * 100:.1f}%"
)

k3.metric(
    "Number of Respondents",
    df.shape[0]
)

# --------------------------------------------------
# Visualization 1: Average Behaviour Scores
# --------------------------------------------------
st.subheader("Average Information-Seeking Behaviour Scores")

fig1 = px.bar(
    df[awareness_cols].mean().reset_index(),
    x="index",
    y=0,
    labels={"index": "Behaviour", "0": "Average Score"},
    title="Average Scores of Consumer Awareness Behaviours"
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "Price comparison and information searching show the highest average scores, "
    "indicating that students are moderately proactive consumers before purchasing."
)

# --------------------------------------------------
# Visualization 2: Histogram
# --------------------------------------------------
st.subheader("Distribution of Consumer Awareness Score")

fig2 = px.histogram(
    df,
    x="Consumer_Awareness_Score",
    nbins=10,
    title="Distribution of Consumer Awareness Scores"
)

st.plotly_chart(fig2, use_container_width=True)

st.write(
    "Most students fall within the medium-to-high awareness range, suggesting partial "
    "but inconsistent information-seeking behaviour."
)

# --------------------------------------------------
# Visualization 3: Box Plot (Age)
# --------------------------------------------------
st.subheader("Consumer Awareness by Age")

fig3 = px.box(
    df,
    x="Age",
    y="Consumer_Awareness_Score",
    title="Consumer Awareness Score Across Age Groups"
)

st.plotly_chart(fig3, use_container_width=True)

st.write(
    "Older students tend to exhibit slightly higher awareness scores, possibly due to "
    "greater purchasing experience."
)

# --------------------------------------------------
# Visualization 4: Awareness by Faculty
# --------------------------------------------------
st.subheader("Consumer Awareness by Faculty")

faculty_avg = (
    df.groupby("Faculty")["Consumer_Awareness_Score"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    faculty_avg,
    x="Faculty",
    y="Consumer_Awareness_Score",
    title="Average Consumer Awareness Score by Faculty"
)

st.plotly_chart(fig4, use_container_width=True)

st.write(
    "Differences across faculties suggest that academic background may influence "
    "consumer awareness and information-seeking behaviour."
)

# --------------------------------------------------
# Visualization 5: Correlation Heatmap
# --------------------------------------------------
st.subheader("Correlation Between Awareness Behaviours")

corr = df[awareness_cols].corr()

fig5, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap of Consumer Awareness Variables")

st.pyplot(fig5)

st.write(
    "Strong positive correlations indicate that students who actively search for "
    "information also tend to compare prices and read agreements carefully."
)
