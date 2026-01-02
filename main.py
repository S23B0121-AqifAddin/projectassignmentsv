import streamlit as st

st.set_page_config(
    page_title="Financial Behaviour among University Students"
)

# Define each page
page_1 = st.Page("page1.py", title="(Aisyah) Budgeting & Spending Behavior")
page_2 = st.Page("page2.py", title="(Aqif) Financial Decision-Making")
page_3 = st.Page("page3.py", title="(Khadijah) Consumer Rights", icon=":material/receipt_long:")
page_4 = st.Page("page4.py", title="(Kisantini) Consumer Awareness & Information Seeking")

# Create navigation menu
pg = st.navigation(
    {
        "Menu": [page_1, page_2, page_3, page_4]
    }
)

# -------- HOMEPAGE CONTENT --------
if pg.current_page is None:
    st.title("💷 Financial Behaviour among University Students")

    st.markdown("""
    ### Group Overview
    This dashboard presents an analysis of **financial behaviour among university students**.

    Click a section below to view each member’s contribution.
    """)

    st.divider()

    # Button layout (2x2 grid)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Aisyah – Budgeting & Spending Behaviour", use_container_width=True):
            pg.switch_page(page_1)

        if st.button("🧠 Aqif – Financial Decision-Making", use_container_width=True):
            pg.switch_page(page_2)

    with col2:
        if st.button("🧾 Khadijah – Consumer Rights", use_container_width=True):
            pg.switch_page(page_3)

        if st.button("🔍 Kisantini – Consumer Awareness", use_container_width=True):
            pg.switch_page(page_4)
            
pg.run()
