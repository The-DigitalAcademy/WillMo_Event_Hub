import streamlit as st
from app_pages.book import book
from app_pages.create import create

def list_events():
    st.title("List of Events")


if st.button("Go to Book"):
        book()
if st.button("Go to Create"):
        create()
