import streamlit as st


if st.button("Booking"):
    st.switch_page("app_pages/book.py")
if st.button("Create Event"):
    st.switch_page("app_pages/create.py")