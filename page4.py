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

# Stop if no records
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

# =========================
# INSIGHT SUMMARY BOX (NEW)
# =========================
st.markdown("### Filter-Based Insight Summary")

# Breakdown complaint categories
never_count = (filtered_df["Complaint_for_Unsuitable_Product"] == "Never").sum()
sometimes_count = (filtered_df["Complaint_for_Unsuitable_Product"] == "Sometimes").sum()
always_count = (filtered_df["Complaint_for_Unsuitable_Product"] == "Always").sum()

most_common = filtered_df["Complaint_for_Unsuitable_Product"].mode()
most_common_value = most_common.iloc[0] if len(most_common) > 0 else "N/A"

# Faculty with highest complaint engagement
faculty_summary = (
    filtered_df.assign(
        Complaint_Engaged=filtered_df["Complaint_for_Unsuitable_Product"].isin(["Always", "Sometimes"])
    )
    .groupby("Faculty")["Complaint_Engaged"]
    .mean()
    .sort_values(ascending=False)
)

top_faculty = faculty_summary.index[0] if len(faculty_summary) > 0 else "N/A"
top_faculty_rate = (faculty_summary.iloc[0] * 100) if len(faculty_summary) > 0 else 0

# Create summary box
st.info(
    f"**Current filter results (n = {total_students})** show that the most common complaint behaviour is "
    f"**{most_common_value}**. Under these filters, **{pct(never_count, total_students):.1f}%** of students "
    f"**never complain**, while **{pct(sometimes_count, total_students):.1f}%** complain **sometimes** and "
    f"**{pct(always_count, total_students):.1f}%** complain **always**. "
    f"Complaint engagement is currently highest in **{top_faculty}** (**{top_faculty_rate:.1f}%**)."
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

if len(faculty_summary) > 1:
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
# VISUAL 4 : AGE vs AWARENESS (BOXPLOT)
# =========================
st.subheader("4. Consumer Rights Awareness by Age")

# Make sure Age is treated as text/category (prevents boxplot issues)
filtered_df["Age"] = filtered_df["Age"].astype(str)

# ---- Correct scoring maps ----
yesno_map = {"Yes": 1, "No": 0}
complaint_map = {"Never": 0, "Sometimes": 1, "Always": 2}

# Clean spaces (sometimes CSV has " Yes" / "No ")
filtered_df["Read_Agreement_Carefully"] = filtered_df["Read_Agreement_Carefully"].astype(str).str.strip()
filtered_df["Compare_Products_Services"] = filtered_df["Compare_Products_Services"].astype(str).str.strip()
filtered_df["Search_Info_Before_Buying"] = filtered_df["Search_Info_Before_Buying"].astype(str).str.strip()
filtered_df["Complaint_for_Unsuitable_Product"] = filtered_df["Complaint_for_Unsuitable_Product"].astype(str).str.strip()

# Create score columns safely
filtered_df["Read_Agreement_score"] = filtered_df["Read_Agreement_Carefully"].map(yesno_map)
filtered_df["Compare_Products_score"] = filtered_df["Compare_Products_Services"].map(yesno_map)
filtered_df["Search_Info_score"] = filtered_df["Search_Info_Before_Buying"].map(yesno_map)
filtered_df["Complaint_score"] = filtered_df["Complaint_for_Unsuitable_Product"].map(complaint_map)

# Fill missing values so boxplot always has numbers
score_cols = [
    "Read_Agreement_score",
    "Compare_Products_score",
    "Search_Info_score",
    "Complaint_score"
]
filtered_df[score_cols] = filtered_df[score_cols].fillna(0)

# Compute final score
filtered_df["Awareness_Score"] = (
    filtered_df["Read_Agreement_score"]
    + filtered_df["Compare_Products_score"]
    + filtered_df["Search_Info_score"]
)

filtered_df["Consumer_Rights_Score"] = (
    filtered_df["Awareness_Score"] + filtered_df["Complaint_score"]
)

# Remove rows where Age is missing/invalid after filters
plot_age_df = filtered_df.dropna(subset=["Age", "Consumer_Rights_Score"]).copy()

# If still empty, show warning
if plot_age_df.empty:
    st.warning("Not enough valid data to generate the Age vs Consumer Rights boxplot under the current filters.")
else:
    fig5 = px.box(
        plot_age_df,
        x="Age",
        y="Consumer_Rights_Score",
        points="all",
        title="Consumer Rights Score by Age (Awareness + Complaint Action)"
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Interpretation
    age_stats = (
        plot_age_df.groupby("Age")["Consumer_Rights_Score"]
        .agg(["median", "mean", "count"])
        .sort_values("median", ascending=False)
    )

    if len(age_stats) > 1:
        best_age = age_stats.index[0]
        best_median = age_stats.iloc[0]["median"]

        worst_age = age_stats.index[-1]
        worst_median = age_stats.iloc[-1]["median"]

        st.write(
            "This boxplot compares consumer rights performance across age groups (combining awareness and complaint action). "
            f"The **highest median score** is observed in **{best_age}** (median = {best_median:.1f}), while the "
            f"**lowest median score** is observed in **{worst_age}** (median = {worst_median:.1f}). "
            "This indicates that age and experience may influence consumer rights awareness and action."
        )
    else:
        st.write(
            "Only one age category is available under the current filters, so comparison across age groups is limited."
        )
# =========================
# VISUAL 5: AWARENESS vs COMPLAINT ACTION (SCATTER)
# =========================
st.subheader("5. Awareness vs Complaint Action")

# Ensure scores exist (created in Visual 4)
# Awareness_Score: 0–3
# Complaint_score: 0–2

plot_scatter_df = filtered_df.dropna(subset=["Awareness_Score", "Complaint_score"]).copy()

# If not enough data points, prevent blank chart
if len(plot_scatter_df) < 3:
    st.warning(
        "Not enough data under the current filters to display the Awareness vs Complaint Action relationship. "
        "Please expand the filter selection."
    )
else:
    fig_scatter = px.scatter(
        plot_scatter_df,
        x="Awareness_Score",
        y="Complaint_score",
        color="Faculty",
        title="Relationship Between Consumer Awareness and Complaint Action",
        labels={
            "Awareness_Score": "Awareness Score (0–3)",
            "Complaint_score": "Complaint Action Score (0–2)"
        },
        trendline="ols"  # trendline helps show overall relationship
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # =========================
    # Dynamic Interpretation
    # =========================
    avg_awareness = plot_scatter_df["Awareness_Score"].mean()
    avg_complaint = plot_scatter_df["Complaint_score"].mean()

    high_awareness = plot_scatter_df[plot_scatter_df["Awareness_Score"] >= 2]
    high_awareness_complaint_rate = (
        high_awareness["Complaint_score"].ge(1).mean() * 100
        if len(high_awareness) > 0 else 0
    )

    st.write(
        f"This scatter plot examines whether higher consumer rights awareness leads to stronger complaint behaviour "
        f"under the current sidebar filters (**n = {len(plot_scatter_df)}**). "
        f"On average, students show an awareness score of **{avg_awareness:.2f}** (out of 3), "
        f"but complaint action remains lower with an average score of **{avg_complaint:.2f}** (out of 2). "
        f"Among students with **high awareness (score ≥ 2)**, approximately **{high_awareness_complaint_rate:.1f}%** "
        "demonstrate complaint engagement (Complaint score ≥ 1). "
        "Overall, the trend indicates that awareness does not always translate into direct complaint action, "
        "highlighting an awareness–action gap."
    )


# =========================
# DATA TABLE
# =========================
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
