import streamlit as st

st.set_page_config(
    page_title="Financial Behaviour among University Students"
)

# Define each page
Home_page = st.Page("homepage.py", title="Group Overview", icon=":material/groups:")

page_1 = st.Page("page1.py", title="(Aisyah) Budgeting & Spending Behavior")
page_2 = st.Page("page2.py", title="(Aqif) Financial Decision-Making")
page_3 = st.Page("page3.py", title="(Khadijah) Consumer Rights 📜")
page_4 = st.Page("page4.py", title="(Kisantini) Consumer Awareness & Information Seeking")

# Create navigation menu
pg = st.navigation(
    {
        "Homepage": [Home_page],
        "Financial Behaviour": [page_1, page_2, page_3, page_4]
    }
)
            
pg.run()
