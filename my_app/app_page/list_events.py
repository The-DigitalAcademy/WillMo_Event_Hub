import streamlit as st
from app_page.create import create
from app_page.book import book

# Define the main navigation function
def list_events():
    st.title("List of Events")

    # Display the list of events (this could come from your database or a mock list)
    events = [
        {"title": "Art Exhibition", "date": "2025-03-01"},
        {"title": "Charity Run", "date": "2025-03-15"},
        {"title": "Fashion Show", "date": "2025-04-05"},
    ]

    # Display each event in the list
    for event in events:
        st.write(f"**{event['title']}** - {event['date']}")

    # Add a "Go to Create" button
    if st.button("Go to Create"):
        st.session_state.page = "create"  # Set page to 'create'
        

    # Add a "Go to Book" button
    if st.button("Go to Book"):
        st.session_state.page = "book"  # Set page to 'book'
        

# Check which page to display based on session state
if 'page' not in st.session_state:
    st.session_state.page = "list_events"  # Default to list_events page

# Navigation based on session state
if st.session_state.page == "list_events":
    list_events()
elif st.session_state.page == "create":
    create()  # This will navigate to the create event page
elif st.session_state.page == "book":
    book()  # This will navigate to the booking page
