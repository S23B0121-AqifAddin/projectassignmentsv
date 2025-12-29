import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Consumer Awareness & Information Seeking",
    layout="wide"
)

st.header("Consumer Awareness & Information Seeking", divider="grey")
st.subheader("Before Buying Behaviour among University Students")

st.write(
    "This section examines students’ consumer awareness and information-seeking behaviour "
    "before making purchasing decisions. The analysis focuses on whether students actively "
    "seek information, compare alternatives, and read important product details prior to buying."
)

# ==================================================
# LOAD DATASET
# ==================================================
url = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv"
df = pd.read_csv(url)

# ==================================================
# MEMBER B VARIABLES (BEFORE BUYING)
# ==================================================
# Mapping to dataset columns:
# - Reading product information → Read_Agreement_Carefully
# - Comparing alternatives → Compare_Products_Services
# - Seeking information → Search_Info_Before_Buying
# - Comparing prices → Compare_Prices_Before_Buying

awareness_cols = [
    "Read_Agreement_Carefully",
    "Compare_Products_Services",
    "Search_Info_Before_Buying",
    "Compare_Prices_Before_Buying"
]

# ==================================================
# LIKERT SCALE ENCODING
# ==================================================
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

df[awareness_cols] = df[awareness_cols].replace(likert_map)

# Force numeric to avoid TypeError
df[awareness_cols] = df[awareness_cols].apply(
    pd.to_numeric, errors="coerce"
)

# ==================================================
# COMPOSITE AWARENESS SCORE
# ==================================================
df["Consumer_Awareness_Score"] = df[awareness_cols].mean(axis=1, skipna=True)

# ==================================================
# KPI SUMMARY BOXES
# ==================================================
k1, k2, k3 = st.columns(3)

k1.metric(
    "Average Awareness Score",
    f"{df['Consumer_Awareness_Score'].mean():.2f} / 5"
)

k2.metric(
    "High Awareness (≥ 4)",
    f"{(df['Consumer_Awareness_Score'] >= 4).mean() * 100:.1f}%"
)

k3.metric(
    "Total Respondents",
    df.shape[0]
)

# ==================================================
# VISUALIZATION 1: BAR CHART
# ==================================================
st.subheader("Information-Seeking Behaviour Frequency")

avg_scores = df[awareness_cols].mean().reset_index()
avg_scores.columns = ["Behaviour", "Average Score"]

fig1 = px.bar(
    avg_scores,
    x="Behaviour",
    y="Average Score",
    text_auto=".2f",
    title="Average Scores of Information-Seeking Behaviours"
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "Students show relatively strong tendencies to compare prices and search for information "
    "before purchasing. However, careful reading of agreements and detailed product comparison "
    "are slightly less consistent."
)

# ==================================================
# VISUALIZATION 2: HISTOGRAM
# ==================================================
st.subheader("Distribution of Consumer Awareness Score")

fig2 = px.histogram(
    df,
    x="Consumer_Awareness_Score",
    nbins=10,
    title="Distribution of Consumer Awareness Scores"
)

st.plotly_chart(fig2, use_container_width=True)

st.write(
    "The distribution indicates that most students fall within the moderate to high awareness range, "
    "suggesting that while many students are informed consumers, there is still room for improvement."
)

# ==================================================
# VISUALIZATION 3: BOX PLOT (AGE)
# ==================================================
st.subheader("Consumer Awareness vs Age")

fig3 = px.box(
    df,
    x="Age",
    y="Consumer_Awareness_Score",
    title="Consumer Awareness Score Across Age Groups"
)

st.plotly_chart(fig3, use_container_width=True)

st.write(
    "Older students generally demonstrate slightly higher consumer awareness scores, "
    "indicating that experience may contribute to more informed purchasing behaviour."
)

# ==================================================
# VISUALIZATION 4: GROUPED BAR (FACULTY)
# ==================================================
st.subheader("Consumer Awareness by Faculty")

faculty_avg = (
    df.groupby("Faculty", as_index=False)["Consumer_Awareness_Score"]
    .mean()
)

fig4 = px.bar(
    faculty_avg,
    x="Faculty",
    y="Consumer_Awareness_Score",
    text_auto=".2f",
    title="Average Consumer Awareness Score by Faculty"
)

st.plotly_chart(fig4, use_container_width=True)

st.write(
    "Differences in awareness scores across faculties suggest that academic background "
    "may influence how actively students seek information before making purchases."
)

# ==================================================
# VISUALIZATION 5: CORRELATION HEATMAP
# ==================================================
st.subheader("Correlation Between Consumer Awareness Behaviours")

corr = df[awareness_cols].corr()

fig5, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap of Consumer Awareness Variables")

st.pyplot(fig5)

st.write(
    "Strong positive correlations indicate that students who actively search for information "
    "also tend to compare alternatives and read agreements carefully, reflecting consistent "
    "information-seeking behaviour."
)
