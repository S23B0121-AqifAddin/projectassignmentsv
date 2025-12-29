
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Consumer Awareness & Information Seeking",
    layout="wide"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="PLO 2", value="3.3", help="Cognitive Skill", border=True)
col2.metric(label="PLO 3", value="3.5", help="Digital Skill", border=True)
col3.metric(label="PLO 4", value="4.0", help="Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value="4.3", help="Communication Skill", border=True)


try:
    df = pd.read_csv(
        "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/main/processed_financial_capability_data.csv",
        encoding="utf-8"
    )
except UnicodeDecodeError:
    df = pd.read_csv(
        "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/main/processed_financial_capability_data.csv",
        encoding="latin-1"
    )

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Filters")

col_f1, col_f2 = st.columns(2)

gender_filter = col_f1.selectbox(
    "Select Gender",
    options=["All"] + sorted(df["Gender"].dropna().unique().tolist())
)

faculty_filter = col_f2.selectbox(
    "Select Faculty",
    options=["All"] + sorted(df["Faculty"].dropna().unique().tolist())
)

filtered_df = df.copy()

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]

if faculty_filter != "All":
    filtered_df = filtered_df[filtered_df["Faculty"] == faculty_filter]


awareness_cols = [
    "Read_Product_Information",
    "Compare_Alternatives",
    "Ask_Seller_Questions",
    "Seek_Advice_Before_Purchase"
]

filtered_df["Awareness_Score"] = filtered_df[awareness_cols].mean(axis=1)


st.subheader("Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Average Awareness Score", round(filtered_df["Awareness_Score"].mean(), 2))
k2.metric("Highest Score", round(filtered_df["Awareness_Score"].max(), 2))
k3.metric("Lowest Score", round(filtered_df["Awareness_Score"].min(), 2))
k4.metric("Total Respondents", filtered_df.shape[0])


# VISUALIZATION 1 — BAR CHART 

st.subheader("Information-Seeking Behaviour Frequency")

mean_scores = filtered_df[awareness_cols].mean().reset_index()
mean_scores.columns = ["Behaviour", "Average Score"]

fig1 = px.bar(
    mean_scores,
    x="Average Score",
    y="Behaviour",
    orientation="h",
    title="Average Frequency of Information-Seeking Behaviours"
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "The bar chart shows that students frequently engage in multiple "
    "information-seeking behaviours before making purchases, with comparing "
    "alternatives and reading product information being the most common."
)


# VISUALIZATION 2 — HISTOGRAM 

st.subheader("Distribution of Consumer Awareness Score")

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df["Awareness_Score"], bins=10, kde=True, ax=ax2)

ax2.set_xlabel("Awareness Score")
ax2.set_ylabel("Frequency")
ax2.set_title("Distribution of Consumer Awareness Score")

st.pyplot(fig2)

st.write(
    "The histogram indicates that most students have a moderate to high "
    "consumer awareness score, suggesting generally proactive pre-purchase behaviour."
)


# VISUALIZATION 3 — BOX PLOT

st.subheader("Consumer Awareness by Age Group")

fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.boxplot(
    x="Age",
    y="Awareness_Score",
    data=filtered_df,
    ax=ax3
)

ax3.set_title("Awareness Score across Age Groups")

st.pyplot(fig3)

st.write(
    "Older students tend to exhibit slightly higher awareness scores, "
    "which may be influenced by greater purchasing experience."
)


# VISUALIZATION 4 — GROUPED BAR

st.subheader("Consumer Awareness by Faculty")

faculty_mean = (
    filtered_df.groupby("Faculty")["Awareness_Score"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    faculty_mean,
    x="Faculty",
    y="Awareness_Score",
    title="Average Consumer Awareness Score by Faculty"
)

st.plotly_chart(fig4, use_container_width=True)

st.write(
    "Differences in awareness scores across faculties suggest that "
    "educational background may influence consumer information-seeking behaviour."
)


# VISUALIZATION 5 — CORRELATION HEATMAP

st.subheader("Correlation between Awareness Variables")

corr = filtered_df[awareness_cols].corr()

fig5, ax5 = plt.subplots(figsize=(6, 5))
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax5
)

ax5.set_title("Correlation Heatmap of Consumer Awareness Variables")

st.pyplot(fig5)

st.write(
    "Strong positive correlations are observed between several information-seeking "
    "behaviours, indicating that students who read product information are also "
    "likely to compare alternatives and seek advice."
)

# ---------------- OVERALL INTERPRETATION ----------------
st.subheader("Overall Analysis & Interpretation")

st.write(
    "Overall, the analysis shows that university students demonstrate a moderate "
    "to high level of consumer awareness and actively seek information before "
    "making purchasing decisions. While most students engage in multiple "
    "information-seeking behaviours, variations across age and faculty suggest "
    "that experience and academic background may play a role in shaping consumer behaviour."
)
