import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Consumer Rights & Complaint Behaviour",
    layout="wide"
)

sns.set(style="whitegrid")

# =========================
# PAGE HEADER
# =========================
st.title("Consumer Rights & Complaint Behaviour")

st.markdown(
    """
    **Individual Goal:**  
    To investigate students’ awareness of consumer rights and complaint behaviour.

    **Problem Definition:**  
    Do students understand and exercise their consumer rights when facing unsuitable products or services?
    """
)

st.divider()

# =========================
# LOAD DATA
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
st.sidebar.header("Filter Options")

gender_options = sorted(df["Gender"].dropna().unique())
selected_genders = st.sidebar.multiselect(
    "Select Gender",
    gender_options,
    default=gender_options
)

age_options = sorted(df["Age"].dropna().unique())
selected_ages = st.sidebar.multiselect(
    "Select Age Group",
    age_options,
    default=age_options
)

filtered_df = df[
    (df["Gender"].isin(selected_genders)) &
    (df["Age"].isin(selected_ages))
]

# =========================
# VISUAL 1: BAR CHART
# =========================
st.subheader("1. Complaint Behaviour Frequency")

fig1, ax1 = plt.subplots(figsize=(6,4))
sns.countplot(
    data=filtered_df,
    x="Complaint_for_Unsuitable_Product",
    hue="Complaint_for_Unsuitable_Product",
    palette="viridis",
    legend=False,
    ax=ax1
)
ax1.set_xlabel("")
ax1.set_ylabel("Number of Students")
st.pyplot(fig1)

st.write(
    "This chart shows how frequently students make complaints when they receive unsuitable products. "
    "After applying filters, changes in the distribution reflect how complaint behaviour differs across "
    "demographic groups. A high proportion of 'Never' responses indicates limited exercise of consumer rights."
)

st.divider()

# =========================
# VISUAL 2: PIE CHART
# =========================
st.subheader("2. Awareness vs Action Gap")

col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots()
    filtered_df["Read_Agreement_Carefully"].value_counts().plot.pie(
        autopct="%1.1f%%",
        startangle=90,
        ax=ax2
    )
    ax2.set_ylabel("")
    ax2.set_title("Reading Agreements Carefully")
    st.pyplot(fig2)

with col2:
    fig3, ax3 = plt.subplots()
    filtered_df["Complaint_for_Unsuitable_Product"].value_counts().plot.pie(
        autopct="%1.1f%%",
        startangle=90,
        ax=ax3
    )
    ax3.set_ylabel("")
    ax3.set_title("Making Complaints")
    st.pyplot(fig3)

st.write(
    "The comparison highlights a clear gap between consumer awareness and action. While many students read agreements "
    "carefully, fewer take action by making formal complaints. This gap remains visible even after demographic filtering."
)

st.divider()

# =========================
# VISUAL 3: STACKED BAR BY FACULTY
# =========================
st.subheader("3. Complaint Behaviour by Faculty")

faculty_data = (
    filtered_df
    .groupby(["Faculty", "Complaint_for_Unsuitable_Product"])
    .size()
    .unstack(fill_value=0)
)

fig4, ax4 = plt.subplots(figsize=(8,5))
faculty_data.plot(kind="bar", stacked=True, colormap="viridis", ax=ax4)
ax4.set_xlabel("Faculty")
ax4.set_ylabel("Number of Students")
ax4.set_title("Complaint Behaviour Across Faculties")
st.pyplot(fig4)

st.write(
    "This visual shows how complaint behaviour differs across faculties. Some faculties display higher engagement "
    "in complaint actions, while others are dominated by students who never complain. This suggests uneven exposure "
    "to consumer rights knowledge across academic disciplines."
)

st.divider()

# =========================
# VISUAL 4: BOX PLOT (AGE)
# =========================
st.subheader("4. Consumer Rights Awareness Score by Age")

mapping = {"Always": 2, "Sometimes": 1, "Never": 0}

rights_cols = [
    "Read_Agreement_Carefully",
    "Compare_Products_Services",
    "Search_Info_Before_Buying",
    "Complaint_for_Unsuitable_Product"
]

for col in rights_cols:
    filtered_df[col + "_score"] = filtered_df[col].map(mapping)

filtered_df["Consumer_Rights_Score"] = filtered_df[
    [c + "_score" for c in rights_cols]
].sum(axis=1)

fig5, ax5 = plt.subplots(figsize=(6,4))
sns.boxplot(
    data=filtered_df,
    x="Age",
    y="Consumer_Rights_Score",
    palette="viridis",
    ax=ax5
)
ax5.set_xlabel("Age Group")
ax5.set_ylabel("Consumer Rights Awareness Score")
st.pyplot(fig5)

st.write(
    "The box plot indicates that older students generally have higher and more consistent consumer rights awareness "
    "scores. Younger age groups show wider variation, suggesting inconsistent understanding and application of rights."
)

st.divider()

# =========================
# VISUAL 5: HEATMAP
# =========================
st.subheader("5. Correlation Between Consumer Rights Behaviours")

corr_df = filtered_df[[c + "_score" for c in rights_cols]]

fig6, ax6 = plt.subplots(figsize=(6,4))
sns.heatmap(
    corr_df.corr(),
    annot=True,
    cmap="RdBu_r",
    center=0,
    fmt=".2f",
    ax=ax6
)
st.pyplot(fig6)

st.write(
    "The heatmap shows strong correlations between information-seeking behaviours, while complaint behaviour "
    "has weaker correlations with other actions. This suggests that awareness does not always lead to active "
    "exercise of consumer rights."
)

# =========================
# DATA SUMMARY
# =========================
st.divider()
st.subheader("Filtered Data Summary")

st.write(
    f"A total of **{len(filtered_df)} respondents** are included based on the selected filters. "
    "All visuals above update dynamically to support focused interpretation."
)

if st.checkbox("Show Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
