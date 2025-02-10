import streamlit as st

# Set up the page title
st.title("Create an Event")
st.write("Fill in the details to create a new event.")

# Form for creating a new event
event_title = st.text_input("Event Title")
event_date = st.date_input("Event Date")
event_location = st.text_input("Event Location")
event_description = st.text_area("Event Description")

# Button to submit the new event
create_button = st.button("Create Event")

if create_button:
    # Here you could add logic to save the event to a database or a file.
    st.success(f"New event '{event_title}' created successfully!")
    st.write(f"**Date**: {event_date}")
    st.write(f"**Location**: {event_location}")
    st.write(f"**Description**: {event_description}")
