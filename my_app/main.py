import streamlit as st
from datetime import datetime


#image_path = "/Users/tshmacm1172/Downloads/WillMo.jpg"
#st.image(image_path, width=290)
#st.set_page_config(page_title="Willcome to WillMo Events",  layout="wide")
pages = [
    st.Page("app_pages/admin.py", title="Admin"),
   st.Page("app_pages/profile.py", title="Profile"),
]

# Adding pages to the sidebar navigation using st.navigation
pg = st.navigation(pages, position="sidebar", expanded=True)
# Running the app

pg.run()
