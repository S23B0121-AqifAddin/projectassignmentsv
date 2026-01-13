import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Consumer Rights & Complaint Behaviour",
    layout="wide"
)

# =========================
# PAGE TITLE & CONTEXT
# =========================
st.title("Consumer Rights & Complaint Behaviour")

st.markdown("""
**Individual Goal:**  
To investigate students’ awareness of consumer rights and complaint behaviour.

**Problem Definition:**  
Do students understand and exercise their consumer rights when facing unsuitable products or services?
""")

st.divider()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    url = (
        "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/processed%20data%20(KIisantini).csv"
    )
    return pd.read_csv(url, encoding="utf-8")

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filter Options")

gender_filter = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

age_filter = st.sidebar.multiselect(
    "Age",
    sorted(df["Age"].dropna().unique()),
    default=sorted(df["Age"].dropna().unique())
)

faculty_filter = st.sidebar.multiselect(
    "Faculty",
    sorted(df["Faculty"].dropna().unique()),
    default=sorted(df["Faculty"].dropna().unique())
)

income_filter = st.sidebar.multiselect(
    "Monthly Income",
    sorted(df["Monthly_Income"].dropna().unique()),
    default=sorted(df["Monthly_Income"].dropna().unique())
)

filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].isin(age_filter)) &
    (df["Faculty"].isin(faculty_filter)) &
    (df["Monthly_Income"].isin(income_filter))
].copy()

# =========================
# HELPER FUNCTIONS
# =========================
def pct(part, whole):
    return 0 if whole == 0 else (part / whole) * 100

# Stop if no records after filtering
if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

# ==================
# KPI SUMMARY BOXES
# ==================
st.subheader("Key Performance Indicators (KPIs)")

total_students = len(filtered_df)

# Complaint behaviour (action-based)
complaint_rate = (
    filtered_df["Complaint_for_Unsuitable_Product"]
    .isin(["Always", "Sometimes"])
    .mean() * 100
)

# Awareness behaviours (Yes/No based)
agreement_reading_rate = (
    (filtered_df["Read_Agreement_Carefully"] == "Yes")
    .mean() * 100
)

info_search_rate = (
    (filtered_df["Search_Info_Before_Buying"] == "Yes")
    .mean() * 100
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Respondents", total_students)
kpi2.metric("Complaint Engagement (%)", f"{complaint_rate:.1f}")
kpi3.metric("Read Agreement (%)", f"{agreement_reading_rate:.1f}")
kpi4.metric("Search Info Before Buying (%)", f"{info_search_rate:.1f}")

st.caption(
    "KPIs reflect awareness (reading agreements, searching information) "
    "and action (making complaints) under current filters."
)

st.divider()

# =========================
# VISUAL 1: COMPLAINT FREQUENCY
# =========================
st.subheader("1. Complaint Behaviour Frequency")

fig1 = px.histogram(
    filtered_df,
    x="Complaint_for_Unsuitable_Product",
    category_orders={
        "Complaint_for_Unsuitable_Product": ["Never", "Sometimes", "Always"]
    },
    color="Complaint_for_Unsuitable_Product",
    title="Complaint Behaviour for Unsuitable Products",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# Dynamic interpretation
never_count = (filtered_df["Complaint_for_Unsuitable_Product"] == "Never").sum()
sometimes_count = (filtered_df["Complaint_for_Unsuitable_Product"] == "Sometimes").sum()
always_count = (filtered_df["Complaint_for_Unsuitable_Product"] == "Always").sum()

most_common = filtered_df["Complaint_for_Unsuitable_Product"].mode()
most_common_value = most_common.iloc[0] if len(most_common) > 0 else "N/A"

st.write(
    f"Based on the current sidebar filters (**n = {total_students} respondents**), "
    f"the most common complaint behaviour is **{most_common_value}**. "
    f"Specifically, **{pct(never_count, total_students):.1f}%** of students **never complain**, "
    f"while **{pct(sometimes_count, total_students):.1f}%** complain **sometimes**, "
    f"and **{pct(always_count, total_students):.1f}%** complain **always**. "
    "This indicates that a noticeable portion of students may not fully exercise their consumer rights through formal complaints."
)

st.divider()

# =========================
# VISUAL 2: AWARENESS VS ACTION (FUNNEL)
# =========================
st.subheader("2. Awareness vs Action Funnel")

search_yes = (filtered_df["Search_Info_Before_Buying"] == "Yes").sum()
read_yes = (filtered_df["Read_Agreement_Carefully"] == "Yes").sum()
complaint_active = filtered_df["Complaint_for_Unsuitable_Product"].isin(["Always", "Sometimes"]).sum()

funnel_df = pd.DataFrame({
    "Stage": [
        "Total Students",
        "Search Info Before Buying",
        "Read Agreement Carefully",
        "Make Complaint"
    ],
    "Count": [
        total_students,
        search_yes,
        read_yes,
        complaint_active
    ]
})

fig_funnel = px.funnel(
    funnel_df,
    x="Count",
    y="Stage",
    title="Drop-off from Consumer Awareness to Action"
)

st.plotly_chart(fig_funnel, use_container_width=True)

drop_read_to_complain = pct(complaint_active, read_yes) if read_yes > 0 else 0

st.write(
    f"Under the selected filters (**n = {total_students}**), "
    f"**{pct(search_yes, total_students):.1f}%** of students search for information before buying, "
    f"and **{pct(read_yes, total_students):.1f}%** read agreements carefully. "
    f"However, only **{pct(complaint_active, total_students):.1f}%** actively make complaints "
    "(Always/Sometimes). "
    f"This suggests an awareness–action gap, where only **{drop_read_to_complain:.1f}%** of students who read agreements "
    "take complaint action."
)

st.divider()

# =========================
# VISUAL 3: FACULTY COMPARISON
# =========================
st.subheader("3. Complaint Behaviour by Faculty")

fig4 = px.histogram(
    filtered_df,
    x="Faculty",
    color="Complaint_for_Unsuitable_Product",
    barmode="stack",
    title="Complaint Behaviour Across Faculties"
)
st.plotly_chart(fig4, use_container_width=True)

# Dynamic interpretation (top vs bottom faculty)
faculty_summary = (
    filtered_df.assign(
        Complaint_Engaged=filtered_df["Complaint_for_Unsuitable_Product"].isin(["Always", "Sometimes"])
    )
    .groupby("Faculty")["Complaint_Engaged"]
    .mean()
    .sort_values(ascending=False)
)

if len(faculty_summary) > 1:
    top_faculty = faculty_summary.index[0]
    top_faculty_rate = faculty_summary.iloc[0] * 100

    lowest_faculty = faculty_summary.index[-1]
    lowest_faculty_rate = faculty_summary.iloc[-1] * 100

    st.write(
        "This visual compares complaint behaviour across faculties under the current filters. "
        f"The **highest complaint engagement** is observed in **{top_faculty}** "
        f"({top_faculty_rate:.1f}% Sometimes/Always), while the **lowest engagement** is in **{lowest_faculty}** "
        f"({lowest_faculty_rate:.1f}%). "
        "This may indicate differences in consumer awareness, confidence, or willingness to take action among faculties."
    )
else:
    st.write(
        "This visual shows complaint behaviour across faculty groups under current filters. "
        "However, only one faculty category is available after filtering, so comparisons across faculties are limited."
    )

st.divider()

# =========================
# VISUAL 4: AGE VS RIGHTS SCORE (BOXPLOT)
# =========================
st.subheader("4. Consumer Rights Awareness by Age")

# Correct scoring maps (Do not change chart type)
yesno_map = {"Yes": 1, "No": 0}
complaint_map = {"Never": 0, "Sometimes": 1, "Always": 2}

filtered_df["Read_Agreement_score"] = filtered_df["Read_Agreement_Carefully"].map(yesno_map)
filtered_df["Compare_Products_score"] = filtered_df["Compare_Products_Services"].map(yesno_map)
filtered_df["Search_Info_score"] = filtered_df["Search_Info_Before_Buying"].map(yesno_map)
filtered_df["Complaint_score"] = filtered_df["Complaint_for_Unsuitable_Product"].map(complaint_map)

filtered_df["Consumer_Rights_Score"] = (
    filtered_df["Read_Agreement_score"]
    + filtered_df["Compare_Products_score"]
    + filtered_df["Search_Info_score"]
    + filtered_df["Complaint_score"]
)

fig5 = px.box(
    filtered_df,
    x="Age",
    y="Consumer_Rights_Score",
    title="Consumer Rights Awareness Score by Age"
)
st.plotly_chart(fig5, use_container_width=True)

# Dynamic interpretation using median
age_stats = (
    filtered_df.groupby("Age")["Consumer_Rights_Score"]
    .agg(["median", "mean", "count"])
    .sort_values("median", ascending=False)
)

if len(age_stats) > 1:
    best_age = age_stats.index[0]
    best_median = age_stats.iloc[0]["median"]

    worst_age = age_stats.index[-1]
    worst_median = age_stats.iloc[-1]["median"]

    st.write(
        "This boxplot summarizes consumer rights awareness scores across age groups based on current filters. "
        f"The age group with the **highest median score** is **{best_age}** (median = {best_median:.1f}), "
        f"while the **lowest median score** is **{worst_age}** (median = {worst_median:.1f}). "
        "This suggests that older or more experienced students may demonstrate stronger consumer rights awareness and behaviour."
    )
else:
    st.write(
        "This boxplot shows consumer rights awareness scores by age, but only one age category is available "
        "after filtering, so comparisons between age groups are limited."
    )

st.divider()

# =========================
# VISUAL 5: CORRELATION HEATMAP
# =========================
st.subheader("5. Relationship Between Consumer Rights Behaviours")

corr_df = filtered_df[
    ["Read_Agreement_score", "Compare_Products_score", "Search_Info_score", "Complaint_score"]
].corr()

fig6 = px.imshow(
    corr_df,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    title="Correlation Between Consumer Rights Behaviours"
)
st.plotly_chart(fig6, use_container_width=True)

# Dynamic interpretation for strongest correlation
corr_pairs = corr_df.unstack().sort_values(ascending=False)
corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) != corr_pairs.index.get_level_values(1)]

if len(corr_pairs) > 0:
    top_pair = corr_pairs.index[0]
    top_value = corr_pairs.iloc[0]

    st.write(
        "This heatmap shows relationships between consumer rights behaviours under the selected filters. "
        f"The strongest relationship appears between **{top_pair[0]}** and **{top_pair[1]}** "
        f"(correlation = {top_value:.2f}). "
        "Overall, awareness-related behaviours tend to move together, but complaint behaviour may remain weaker—"
        "reinforcing that awareness does not always translate into action."
    )
else:
    st.write(
        "This heatmap summarizes behavioural relationships, but correlation interpretation is limited "
        "because the filtered dataset contains insufficient variation."
    )

# =========================
# DATA TABLE
# =========================
st.divider()
st.subheader("Filtered Dataset")

st.write(f"Total records shown: **{len(filtered_df)}**")

if st.checkbox("Show Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)

# =========================
# PAGE NAVIGATION BUTTONS
# =========================
st.divider()
st.write("Click a section below to view another page.")

col1, col2 = st.columns(2)

with col1:
    if st.button("👥 Group Overview", use_container_width=True):
        st.switch_page("homepage.py")

    if st.button("🧠 Aqif – Financial Decision-Making", use_container_width=True):
        st.switch_page("page2.py")

with col2:
    if st.button("📊 Aisyah – Budgeting & Spending Behaviour", use_container_width=True):
        st.switch_page("page1.py")

    if st.button("🧾 Khadijah – Consumer Rights", use_container_width=True):
        st.switch_page("page3.py")
