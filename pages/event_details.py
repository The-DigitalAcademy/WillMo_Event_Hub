import streamlit as st
from establish_connection import connect_to_database
import os
from streamlit_extras.switch_page_button import switch_page

def get_event_details(event_id):
    """Fetch details for a specific event based on event_id."""
    conn = connect_to_database()
    if conn is None:
        return {}

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.event_id, e.image, e.description, e.price, e.quantity, e.event_url,
                   e.event_title, l.venue_title, l.city, l.province, e.start_date, e.start_time
            FROM "Events" as e
            LEFT JOIN "Location" as l ON l.location_id = e.location_id
            WHERE e.event_id = %s;
        ''', (event_id,))
        event = cursor.fetchone()

        if event:
            col_names = [desc[0] for desc in cursor.description]
            return dict(zip(col_names, event))
        else:
            return {}

    except Exception as e:
        st.error(f"Error fetching event details: {e}")
        return {}

    finally:
        cursor.close()
        conn.close()

# CSS for styling the event details page
st.markdown(
    """
    <style>
    .details-container { margin-top: 20px; }
    .details-title { font-size: 24px; font-weight: bold; }
    .details-description { font-size: 16px; margin-top: 10px; }
    .details-price { font-size: 18px; font-weight: bold; color: #444; margin-top: 10px; }
    .details-venue, .details-city, .details-province { font-size: 16px; margin-top: 5px; }
    .details-date-time { font-size: 16px; margin-top: 5px; }
    </style>
    """,
    unsafe_allow_html=True
)

def display_event_details_page():
    """Displays the detailed information for a selected event."""
    # Get the event ID from session state
    event_id = st.session_state.get("event_id")
    
    if not event_id:
        st.error("No event selected.")
        return

    # Fetch event details from the database
    event = get_event_details(event_id)

    if not event:
        st.error("Event not found.")
        return

    # Display event details
    st.subheader("Event Details")

    # Event image (if available) with resized image width
    image_path = event['image']
    if image_path and not image_path.startswith("http"):
        local_image_path = f".{image_path}"
        if os.path.exists(local_image_path):
            st.image(local_image_path, caption=event['event_title'], use_container_width=True, width=600)  # Use the new parameter
        else:
            st.warning(f"Image not found: {local_image_path}")
    elif image_path and image_path.startswith("http"):
        st.image(image_path, caption=event['event_title'], use_container_width=True, width=600)  # Use the new parameter

    # Display event details in a structured format
    st.markdown(f'<div class="details-title">{event["event_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-description">{event["description"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-price">Price: R{event["price"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-venue">Venue: {event["venue_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-city">City: {event["city"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-province">Province: {event["province"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-date-time">Date: {event["start_date"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="details-date-time">Time: {event["start_time"]}</div>', unsafe_allow_html=True)
    
    # If the event has a URL, provide a link
    if event.get("event_url"):
        st.markdown(f'[Visit Event Page]({event["event_url"]})', unsafe_allow_html=True)
    
    # "Book Now" button to switch to car page
    if st.button("Book Now"):
        switch_page("checkout")

# Run the function to display the event details page
display_event_details_page()
