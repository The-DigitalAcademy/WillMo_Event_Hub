import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        switch_page("Signup")  # Redirect to login page if not logged in

# Event-Hub Page Function
def event_hub_page():
    # Ensure the user is logged in before accessing this page
    check_logged_in()

    st.title("Event Hub")

    # Show the options to Book or Create an Event
    st.write("Choose an option:")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Book Event"):
            switch_page("event1")  # Redirect to Bookings page

    with col2:
        if st.button("Create Event"):
            switch_page("create_event")  # Redirect to Create Event page

# Call the function to display the Event Hub page
event_hub_page()
