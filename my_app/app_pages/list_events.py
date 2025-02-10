import streamlit as st


if st.button("Booking"):
    st.switch_page("app_pages/book.py")
if st.button("List Events"):
    st.switch_page("app_pages/list_events.py")