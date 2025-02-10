import streamlit as st
from app_pages.list_events import list_events

#image_path = "/Users/tshmacm1172/Downloads/WillMo.jpg"
#st.image(image_path, width=290)
#st.set_page_config(page_title="Willcome to WillMo Events",  layout="wide")
# Conditionally hide the "Create Yoor Event" page
show_create_page = False  # Set this to False to hide the page, True to show

# Define the pages
pages = [
    st.Page("app_pages/home.py", title="Home"),
    st.Page("app_pages/admin.py", title="Admin"),
    st.Page("app_pages/profile.py", title="Profile"),
    st.Page("app_pages/list_events.py", title="List Events"),
    st.Page("app_pages/events.py", title="Events"),
]

# Adding pages to the sidebar navigation using st.navigation
pg = st.navigation(pages, position="sidebar", expanded=True)

# Running the app
pg.run()

