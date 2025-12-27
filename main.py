import streamlit as st

st.set_page_config(page_title="Financial Behaviour among University Students")

# Define each page
page_1 = st.Page("page1.py", title="Budgeting & Spending Behavior")
page_2 = st.Page("page2.py", title="Page 2")
page_3 = st.Page("page3.py", title="Consumer Rights")
page_4 = st.Page("page4.py", title="Page 4")

# Create navigation menu
pg = st.navigation(
    {
        "Menu": [page_1, page_2, page_3, page_4]
    }
)

pg.run()
