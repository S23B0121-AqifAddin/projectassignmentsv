import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Consumer Awareness Dashboard", layout="wide")

# =========================
# PAGE HEADER
# =========================
st.header("Financial Behaviour among University Students", divider="grey")

col1, col2, col3, col4 = st.columns(4)
col1.metric("PLO 2", "3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric("PLO 3", "3.5", help="PLO 3: Digital Skill", border=True)
col3.metric("PLO 4", "4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric("PLO 5", "4.3", help="PLO 5: Communication Skill", border=True)

# =========================
# LOAD PROCESSED DATA ONLY
# =========================
@st.cache_data
def load_data():
    url = (
        "https://raw.githubusercontent.com/"
        "S23B0121-AqifAddin/projectassignmentsv/"
        "main/Datasets/(Kisa)processed_financial_capability_data%20(3).csv"
    )
    return pd.read_csv(url, encoding="utf-8")

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Data Controls")

# Gender filter
gender_options = sorted(df["Gender"].dropna().unique())
selected_genders = st.sidebar.multiselect(
    "Filter by Gender",
    gender_options,
    default=gender_options
)

# Age filter
age_options = sorted(df["Age"].dropna().unique())
selected_ages = st.sidebar.multiselect(
    "Filter by Age",
    age_options,
    default=age_options
)

# Apply filters
filtered_df = df[
    (df["Gender"].isin(selected_genders)) &
    (df["Age"].isin(selected_ages))
]

# =========================
# MAIN TITLE
# =========================
st.title("Consumer Awareness & Information-Seeking Behaviour")

# =========================
# DOWNLOAD BUTTON
# =========================
st.sidebar.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False).encode("utf-8"),
    "filtered_consumer_data.csv",
    "text/csv"
)

# =========================
# VISUAL FUNCTION
# =========================
def create_plot(column, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=filtered_df,
        x=column,
        hue=column,
        palette="viridis",
        legend=False,
        ax=ax
    )
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Number of Students")
    plt.xticks(rotation=30)
    st.pyplot(fig)

# =========================
# VISUAL DASHBOARD
# =========================
col1, col2 = st.columns(2)

with col1:
    create_plot(
        "Search_Info_Before_Buying",
        "Searching for Information Before Buying"
    )

    create_plot(
        "Compare_Prices_Before_Buying",
        "Comparing Prices Before Buying"
    )

with col2:
    create_plot(
        "Compare_Products_Services",
        "Comparing Products or Services"
    )

    create_plot(
        "Read_Agreement_Carefully",
        "Reading Agreements Carefully"
    )

# =========================
# DATA SUMMARY
# =========================
st.divider()
st.subheader("Data Overview")

st.write(
    f"The analysis currently displays **{len(filtered_df)} respondents** "
    "based on the selected age and gender filters. All visualisations above "
    "update dynamically according to these selections."
)

if st.checkbox("Show Filtered Data Table"):
    st.dataframe(filtered_df, use_container_width=True)
