import streamlit as st

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        switch_page("Signup")  # Redirect to login page if not logged in


def get_event_image(event_id):
    """Fetch the image URL/path for a specific event."""
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT image FROM "Events" WHERE event_id = %s', (event_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    st.error("Database connection failed.")
    return None
def display_event(event_id):
    """Display event details including the image."""
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT event_title, description, start_date, start_time, capacity, quantity, price, event_url, image
                FROM "Events"
                WHERE event_id = %s
            ''', (event_id,))
            event = cursor.fetchone()
            if event:
                event_title, description, start_date, start_time, capacity, quantity, price, event_url, image = event

                st.subheader(event_title)
                st.write(f"**Description**: {description}")
                st.write(f"**Date**: {start_date}")
                st.write(f"**Time**: {start_time}")
                st.write(f"**Capacity**: {capacity}")
                st.write(f"**Ticket Quantity**: {quantity}")
                st.write(f"**Price**: R{price:.2f}")
                st.write(f"**Event URL**: {event_url}")

                # Display the image
                if image:
                    if image.startswith("http"):  # If it's a URL
                        st.image(image, caption=event_title, use_column_width=True)
                    else:  # If it's a file path
                        st.image(image, caption=event_title, use_column_width=True)
                else:
                    st.warning("No image available for this event.")
            else:
                st.error("Event not found.")
    else:
        st.error("Unable to connect to the database.")