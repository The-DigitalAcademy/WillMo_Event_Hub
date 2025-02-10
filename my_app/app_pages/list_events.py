import streamlit as st


if st.button("Booking"):
    st.page_link("Go to Events", "app_pages/book.py")
if st.button("Create Event"):
    st.page_link("Go to Events", "app_pages/create.py")