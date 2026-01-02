import streamlit as st

st.set_page_config(
    page_title="Financial Behaviour among University Students"
)

# -------- HOMEPAGE CONTENT (GROUP PAGE) --------
st.title("💷 Financial Behaviour among University Students")

st.markdown("""
### Group Overview
This dashboard presents an analysis of **financial behaviour among university students**.

Each section represents the contribution of a group member:
- **(Aisyah)** Budgeting & Spending Behaviour  
- **(Aqif)** Financial Decision-Making  
- **(Khadijah)** Consumer Rights  
- **(Kisantini)** Consumer Awareness & Information Seeking  

Use the navigation menu to explore each section.
""")

st.divider()

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

pg.run()
