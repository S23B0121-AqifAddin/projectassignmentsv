import streamlit as st

st.title("💵💷Financial Behaviour among University Students💴💶")

st.markdown("""
### Group Overview
This dashboard presents an analysis of **financial behaviour among university students**.

Click a section below to view each member’s contribution.
""")

#Load Original Dataset
try:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/Datasets/Financial%20Capability%20around%20Student%20.csv', encoding='latin-1')
df

st.divider()

col1, col2 = st.columns(2)

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
