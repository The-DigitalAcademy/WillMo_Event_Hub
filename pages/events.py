import streamlit as st
import os
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page

# Define the local image directory (update this path accordingly)
IMAGE_FOLDER = "event_images"

def get_upcoming_events():
    """Fetch upcoming events from the database."""
    conn = connect_to_database()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.event_id, e.image, l.province, l.city, e.description, e.price, e.quantity, e.event_url,
                   e.event_title, l.venue_title, e.start_date, e.start_time
            FROM "Events" as e
            LEFT JOIN "Location" as l ON l.location_id = e.location_id
            ORDER BY e.start_date ASC
            LIMIT 6;
        ''')
        events = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in events]

    except Exception as e:
        st.error(f"Error fetching events: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

# CSS for styling the event cards
st.markdown(
    """
    <style>
    .card-title { font-size: 16px; font-weight: bold; margin: 10px 0; }
    .card-details { font-size: 14px; color: #666; }
    .card-price { font-size: 14px; font-weight: bold; margin: 10px 0; color: #444; }
    </style>
    """,
    unsafe_allow_html=True
)

def display_booking_page():
    """Displays the event booking page with search and filter options."""
    st.subheader("Upcoming Events")

    # Fetch upcoming events
    events = get_upcoming_events()

    if not events:
        st.info("No upcoming events found.")
        return

    # Display events in a responsive grid layout
    cols = st.columns(3)
    for idx, event in enumerate(events):
        col = cols[idx % 3]
        with col:
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                
                # Retrieve the image path/URL from the event data
                image_path = event['image']

                # Handle local file paths
                if image_path and not image_path.startswith("http"):
                    # Prepend '.' to make the path relative to the current directory
                    local_image_path = f".{image_path}"
                    if os.path.exists(local_image_path):
                        st.image(local_image_path, caption=event['event_title'], use_container_width=True)
                    else:
                        st.warning(f"Image not found: {local_image_path}")

                # Handle URLs
                elif image_path and image_path.startswith("http"):
                    st.image(image_path, caption=event['event_title'], use_container_width=True)

                # If no image is available
                else:
                    st.warning("No image available for this event.")

                # Display event details
                st.markdown(f'<div class="card-title">{event["event_title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-details">Date: {event["start_date"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-details">Time: {event["start_time"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-details">Venue: {event["venue_title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-details">City: {event["city"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-details">Province: {event["province"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-price">Price: R{event["price"]}</div>', unsafe_allow_html=True)
                
                # "More Details" button to navigate to event details page
                if st.button("More Details", key=f"details_{event['event_id']}"):  # Use event_id for a unique key
                    st.session_state["event_id"] = event['event_id']
                    switch_page("event_details")
                
                st.markdown('</div>', unsafe_allow_html=True)

# Run the function to display the booking page
display_booking_page()