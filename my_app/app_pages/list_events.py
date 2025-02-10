import streamlit as st

# Button to navigate to the 'book.py' page
if st.button("Booking"):
    st.session_state.page = "app_pages/book.py"  # Set a session state for navigation

# Button to navigate to the 'create.py' page
if st.button("Create Event"):
    st.session_state.page = "app_pages/create.py"  # Set a session state for navigation

# Redirect to the selected page (if any)
if "page" in st.session_state:
    st.page_link("Go to Events", destination=st.session_state.page)
