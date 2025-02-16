import streamlit as st
import psycopg2
import os
from datetime import date
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page

    
event_categories = ["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival", "Fashion Event"]

# Function to fetch the most booked events
def get_popular_events():
    """Fetch the most popular events based on booking count."""
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                e.event_id,
                e.event_title,
                e.image,
                l.city,
                l.province,
                c.category,
                e.description,
                e.price,
                e.quantity,
                e.event_url,
                COUNT(bem.booking_id) AS total_bookings
            FROM "Events" e
            JOIN "Location" l ON l.location_id = e.location_id
            JOIN "Category" c ON c.category_id = e.category_id
            JOIN "BookingEventMap" bem ON bem.event_id = e.event_id
            JOIN "Bookings" b ON b.booking_id = bem.booking_id
            GROUP BY e.event_id, l.city, l.province, c.category
            ORDER BY total_bookings DESC
            LIMIT 5;
        ''')

        events = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in events]

    except Exception as e:
        st.error(f"Error fetching popular events: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to fetch upcoming events with filters
def get_upcoming_events(location=None, category=None, start_date=None):
    """Fetch upcoming events based on optional filters."""
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        query = '''
            SELECT 
                e.event_id,
                e.event_title,
                e.image,
                l.city,
                l.province,
                c.category,
                e.description,
                e.price,
                e.quantity,
                e.event_url,
                e.start_date
            FROM "Events" e
            JOIN "Location" l ON l.location_id = e.location_id
            JOIN "Category" c ON c.category_id = e.category_id
            WHERE e.start_date >= %s
        '''
        params = [date.today()]

        if location:
            query += " AND l.city ILIKE %s"
            params.append(f"%{location}%")

        if category:
            query += " AND c.category ILIKE %s"
            params.append(f"%{category}%")

        if start_date:
            query += " AND e.start_date >= %s"
            params.append(start_date)

        query += " ORDER BY e.start_date ASC LIMIT 5;"

        cursor.execute(query, params)
        events = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in events]

    except Exception as e:
        st.error(f"Error fetching upcoming events: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()

def display_event_image(image_path, event_title):
    """Handles both local file paths and URLs for images with size control."""
    if image_path:
        if image_path.startswith("http"):
            st.image(image_path, caption=event_title, use_container_width=False, width=600)
        else:
            local_image_path = os.path.join(os.getcwd(), image_path.lstrip("/"))
            if os.path.exists(local_image_path):
                st.image(local_image_path, caption=event_title, use_container_width=False, width=600)
            else:
                st.warning(f"⚠️ Image not found: {local_image_path}")
    else:
        st.warning("⚠️ No image available for this event.")

# Streamlit App
st.set_page_config(layout="wide")
st.title("Welcome to WillMo Event Hub")

# Filters section header
st.subheader("🔍 Filter Events by Popularity or Date")

# Filters at the top of the page (not in the sidebar)
show_popular = st.checkbox("Show Popular Events", value=False)
show_upcoming = st.checkbox("Show Upcoming Events", value=False)

# Search Filter for Upcoming Events
search_query = st.text_input("🔎 Search Events", key="search_query")

# Location Filter for Upcoming Events
location_filter = st.text_input("📍 Location", key="location_filter")

# Category Filter for Upcoming Events
category_filter = st.selectbox(" Category", event_categories, key="category_filter")

# Date filter for Upcoming Events
start_date_filter = st.date_input("📅 Start Date", value=None, key="start_date_filter")

# Search Button
search_button = st.button("Search Events")

# Left Section - Popular Events or All Events
st.header(" Events")

# Always fetch all events if no filter is selected or show filtered events
all_events = get_upcoming_events(location=location_filter, category=category_filter, start_date=start_date_filter)

# If search button is clicked, apply filters
if search_button:
    if show_popular:
        popular_events = get_popular_events()
        if popular_events:
            st.subheader("Popular Events")
            for event in popular_events:
                with st.container():
                    st.subheader(event['event_title'])
                    display_event_image(event['image'], event['event_title'])
                    st.write(f"📅 **Bookings:** {event['total_bookings']}")
                    st.write(f"📍 **Location:** {event['city']}, {event['province']}")
                    st.write(f"💰 **Price:** R{event['price']}")
                    st.write(f"🎟️ **Tickets Left:** {event['quantity']}")
                    st.markdown(f"[🔗 View Event]({event['event_url']})", unsafe_allow_html=True)
                    st.divider()

    if show_upcoming:
        upcoming_events = get_upcoming_events(location=location_filter, category=category_filter, start_date=start_date_filter)

        # Apply search filter if a search query is entered
        if search_query:
            upcoming_events = [event for event in upcoming_events if search_query.lower() in event['event_title'].lower() or search_query.lower() in event['description'].lower()]

        if upcoming_events:
            st.subheader("Upcoming Events")
            for event in upcoming_events:
                with st.container():
                    st.subheader(event['event_title'])
                    display_event_image(event['image'], event['event_title'])
                    st.write(f"📅 **Date:** {event['start_date']}")
                    st.write(f"📍 **Location:** {event['city']}, {event['province']}")
                    st.write(f"💰 **Price:** R{event['price']}")
                    st.write(f"🎟️ **Tickets Left:** {event['quantity']}")
                    st.markdown(f"[🔗 View Event]({event['event_url']})", unsafe_allow_html=True)
                    st.divider()

else:
    # If no filters and no search are applied, display all events
    if all_events:
        st.subheader("All Upcoming Events")
        for event in all_events:
            with st.container():
                st.subheader(event['event_title'])
                display_event_image(event['image'], event['event_title'])
                st.write(f"📅 **Date:** {event['start_date']}")
                st.write(f"📍 **Location:** {event['city']}, {event['province']}")
                st.write(f"💰 **Price:** R{event['price']}")
                st.write(f"🎟️ **Tickets Left:** {event['quantity']}")
                st.markdown(f"[ View Event]({event['event_url']})", unsafe_allow_html=True)
                st.divider()
    else:
        st.warning("No events found.")

# Section to Create an Event


# List of event categories
st.sidebar.header("Host or Book an event now!")
st.sidebar.write("Do you want to book or create you own event?")
create_event_button = st.sidebar.button("Click here")
if create_event_button:
    switch_page = "WillMo Event Hub" 