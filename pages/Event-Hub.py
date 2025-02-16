import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        switch_page("Signup")

# Event-Hub Page Function
def event_hub_page():
    # Ensure the user is logged
    check_logged_in()

    st.title("Event Hub")


    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Book an Event")
        st.write("Explore and book from a variety of events curated just for you.")
        if st.button("Book Event", key="book_event"):
            switch_page("events")

    with col2:
        st.markdown("#### Create an Event")
        st.write("Have an event idea? Create and promote your own event here.")
        if st.button("Create Event", key="create_event"):
            switch_page("creating_event") 


event_hub_page()
