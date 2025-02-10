import streamlit as st
from pages.events import get_upcoming_events

# Set up the page title
st.title("Book an Event")
st.write("Choose an event to book.")

# Fetch events from events.py
try:
    events = get_upcoming_events()
    st.write(events)  # Debugging: check if events are being fetched correctly
except Exception as e:
    st.error(f"Error fetching events: {e}")

# Display list of upcoming events
if events:
    event_titles = [event['title'] for event in events]
    selected_event = st.selectbox("Select an event to book", event_titles)

    # Show details for the selected event
    if selected_event:
        event_details = next(event for event in events if event['title'] == selected_event)
        st.write(f"**Event**: {event_details['title']}")
        st.write(f"**Date**: {event_details['date']}")
        st.write(f"**Location**: {event_details['location']}")
        st.write(f"**Description**: {event_details['description']}")

        # Simulate booking action
        book_button = st.button("Book this Event")
        if book_button:
            st.success(f"You have successfully booked '{event_details['title']}'!")
else:
    st.write("No events available for booking at the moment. Please check back later.")
