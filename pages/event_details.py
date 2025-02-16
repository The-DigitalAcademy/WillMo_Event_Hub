import os
import streamlit as st
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page

# Function to display event image
def display_event_image(image_path, event_title):
    if image_path:
        if image_path.startswith("http"):
            st.image(image_path, caption=event_title, use_container_width=False, width=1000)
        else:
            local_image_path = os.path.join(os.getcwd(), image_path.lstrip("/"))
            if os.path.exists(local_image_path):
                st.image(local_image_path, caption=event_title, use_container_width=False, width=800)
            else:
                st.warning(f"⚠️ Image not found: {local_image_path}")
    else:
        st.warning("⚠️ No image available for this event.")

# Function to fetch event details
def fetch_event_details(event_id):
    connection = connect_to_database()
    if connection:
        query = """
            SELECT e.event_id, e.event_title, e.image, e.description, e.price, e.quantity, 
                   l.venue_title, l.province, l.city, l.google_maps, c.category
            FROM "Events" e
            INNER JOIN "Category" c ON e.category_id = c.category_id
            INNER JOIN "Location" l ON e.location_id = l.location_id
            WHERE e.event_id = %s
        """
        params = [event_id]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchone()
            if data:
                return {
                    "event_id": data[0], 
                    "event_title": data[1], 
                    "image": data[2], 
                    "description": data[3], 
                    "price": data[4], 
                    "quantity": data[5],
                    "venue_title": data[6],
                    "province": data[7],
                    "city": data[8],
                    "google_maps": data[9],
                    "category": data[10]
                }
    return None

# Event Details Page
def display_event_details():
    # Check if the user is logged in
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        switch_page("Signup")
        return
    
    # Get event ID from session state
    event_id = st.session_state.get("event_id", None)

    if event_id:
        st.title("Event Details")
        event_details = fetch_event_details(event_id)
        if event_details:

            display_event_image(event_details['image'], event_details['event_title'])
            st.header(event_details['event_title'])

            st.subheader("Description")
            st.write(event_details['description'])

            st.subheader("Location")
            st.write(f"**Venue:** {event_details['venue_title']}")
            st.write(f"**City:** {event_details['city']}, {event_details['province']}")
            st.write(f"**Google Maps:** [View Location]({event_details['google_maps']})")

            st.subheader("Ticket Information")
            st.write(f"**Price:** R{event_details['price']}")
            st.write(f"**Available Tickets:** {event_details['quantity']}")

            # Booking Button and Back Button
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button("Go Back", key="go_back"):
                    switch_page("events")

            with col2:
                if st.button("Book Now", key="book_now"):
                    switch_page("checkout")   

        else:
            st.error("Event details not found.")
    else:
        st.error("No event selected.")


display_event_details()
