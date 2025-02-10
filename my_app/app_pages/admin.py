import streamlit as st

# Home Page
def admin():
    # Check if an event has been created
    if 'event_created' not in st.session_state or not st.session_state['event_created']:
        st.write("You must create an event first. Redirecting to the event creation page...")
        st.button("Go to Event Creation", on_click=go_to_create_page)
    else:
        st.write("Welcome to the Admin Page!")
        
        # Display event summary from session state
        event_name = st.session_state['event_name']
        event_date = st.session_state['event_date']
        event_description = st.session_state['event_description']

        st.write(f"**Event Name:** {event_name}")
        st.write(f"**Event Date:** {event_date}")
        st.write(f"**Event Description:** {event_description}")

def go_to_create_page():
    # Redirect to create.py page
    st.experimental_rerun()

if __name__ == "__main__":
    admin()
