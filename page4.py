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
]

# =========================
# KPI SUMMARY BOXES
# =========================
st.subheader("Key Performance Indicators (KPIs)")

total_students = len(filtered_df)

complaint_rate = (
    (filtered_df["Complaint_for_Unsuitable_Product"] == "Always").mean() * 100
)

agreement_reading_rate = (
    (filtered_df["Read_Agreement_Carefully"] == "Always").mean() * 100
)

info_search_rate = (
    (filtered_df["Search_Info_Before_Buying"] == "Always").mean() * 100
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Respondents", total_students)
kpi2.metric("Complaint Rate (%)", f"{complaint_rate:.1f}")
kpi3.metric("Read Agreement (%)", f"{agreement_reading_rate:.1f}")
kpi4.metric("Search Info Before Buying (%)", f"{info_search_rate:.1f}")

st.write(
    "These KPIs summarise students’ consumer rights behaviour under the selected filters. "
    "Changes in filters immediately reflect shifts in complaint activity and awareness-related actions."
)

st.divider()

# =========================
# VISUAL 1: COMPLAINT FREQUENCY
# =========================
st.subheader("1. Complaint Behaviour Frequency")

fig1 = px.histogram(
    filtered_df,
    x="Complaint_for_Unsuitable_Product",
    color="Complaint_for_Unsuitable_Product",
    title="Frequency of Complaints for Unsuitable Products",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

st.write(
    "This bar chart shows how often students make complaints when sold unsuitable products. "
    "Even after applying demographic and income filters, a substantial proportion of students "
    "report that they never complain, indicating limited exercise of consumer rights."
)

st.divider()

# =========================
# VISUAL 2: AWARENESS VS ACTION
# =========================
st.subheader("2. Awareness vs Action Comparison")

col1, col2 = st.columns(2)

with col1:
    fig2 = px.pie(
        filtered_df,
        names="Read_Agreement_Carefully",
        title="Reading Agreements Carefully"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.pie(
        filtered_df,
        names="Complaint_for_Unsuitable_Product",
        title="Making Complaints"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.write(
    "The pie charts highlight a clear awareness–action gap. While many students consistently read agreements, "
    "far fewer take the step of making formal complaints. This pattern remains stable across most filter selections."
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

st.write(
    "This visual shows noticeable differences in complaint behaviour across faculties. "
    "Some faculties demonstrate higher complaint engagement, suggesting stronger consumer awareness, "
    "while others are dominated by non-complaint behaviour."
)

st.divider()

# =========================
# VISUAL 4: AGE VS RIGHTS SCORE
# =========================
st.subheader("4. Consumer Rights Awareness by Age")

score_map = {"Always": 2, "Sometimes": 1, "Never": 0}

rights_cols = [
    "Read_Agreement_Carefully",
    "Compare_Products_Services",
    "Search_Info_Before_Buying",
    "Complaint_for_Unsuitable_Product"
]

for col in rights_cols:
    filtered_df[col + "_score"] = filtered_df[col].map(score_map)

filtered_df["Consumer_Rights_Score"] = filtered_df[
    [c + "_score" for c in rights_cols]
].sum(axis=1)

fig5 = px.box(
    filtered_df,
    x="Age",
    y="Consumer_Rights_Score",
    title="Consumer Rights Awareness Score by Age"
)
st.plotly_chart(fig5, use_container_width=True)

st.write(
    "Older students tend to show higher and more consistent consumer rights scores, while younger students "
    "exhibit wider variation. This suggests that experience plays a role in understanding and exercising rights."
)

st.divider()

# =========================
# VISUAL 5: CORRELATION HEATMAP
# =========================
st.subheader("5. Relationship Between Consumer Rights Behaviours")

corr_df = filtered_df[[c + "_score" for c in rights_cols]].corr()

fig6 = px.imshow(
    corr_df,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    title="Correlation Between Consumer Rights Behaviours"
)
st.plotly_chart(fig6, use_container_width=True)

st.write(
    "Information-seeking behaviours show strong positive relationships with one another. "
    "However, complaint behaviour is less strongly correlated, reinforcing that awareness does not always "
    "translate into action."
)

# =========================
# DATA TABLE
# =========================
st.divider()
st.subheader("Filtered Dataset")

st.write(f"Total records shown: **{len(filtered_df)}**")

if st.checkbox("Show Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)



st.write("""
Click a section below to view another page.
""")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Aisyah – Budgeting & Spending Behaviour", use_container_width=True):
        st.switch_page("page1.py")

    if st.button("🧠 Aqif – Financial Decision-Making", use_container_width=True):
        st.switch_page("page2.py")

with col2:
    if st.button("🧾 Khadijah – Consumer Rights", use_container_width=True):
        st.switch_page("page3.py")

    if st.button("🔍 Kisantini – Consumer Awareness", use_container_width=True):
        st.switch_page("page4.py")

with col3:
    if st.button("👥 Group Overview", use_container_width=True):  # New button
        st.switch_page("homepage.py")  # Replace with your homepage file
