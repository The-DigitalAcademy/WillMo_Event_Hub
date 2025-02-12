import streamlit as st
import pandas as pd
from establish_connection import connect_to_database

st.set_page_config(page_title="WillMo Events Hub", layout="wide")
st.title("WillMo Events Hub")

st.subheader("Search for an Event")

# List of major South African cities for location filter
south_african_cities = [
    "All Locations",
    "Cape Town",
    "Johannesburg",
    "Durban",
    "Pretoria",
    "Port Elizabeth",
    "Bloemfontein",
    "East London",
    "Polokwane",
    "Nelspruit",
    "Kimberley",
    "Pietermaritzburg",
    "Vanderbijlpark",
    "George",
    "Rustenburg",
    "Mbombela",
    "Tshwane",
]

event_title_search = st.text_input("Search by event title", "").strip()

location_search = st.selectbox("Filter by location", south_african_cities)

st.subheader("Upcoming Events")


def get_upcoming_events():
    conn = connect_to_database()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT  l.province, l.city, e.price, e.event_url
            , e.event_title, l.venue_title, e.start_date, e.start_time
            FROM "Events" as e
            LEFT JOIN "Location" as l
            ON l.location_id = e.location_id;
        ''')
        events = cursor.fetchall()

        # Get column names
        col_names = [desc[0] for desc in cursor.description]

        # Convert rows to dictionaries
        event_list = [dict(zip(col_names, row)) for row in events]

        return event_list

    except Exception as e:
        st.error(f"Error fetching events: {e}")
        return []

    finally:
        cursor.close()
        conn.close()


events = get_upcoming_events()

# Filter events based on search inputs
filtered_events = []
for event in events:
    title_match = event_title_search.lower() in event["event_title"].lower() if event_title_search else True
    
    # Safeguard for None value in "city" field
    location_match = location_search == "All Locations" or (event.get("city") and location_search in event["city"])

    if title_match and location_match:
        filtered_events.append(event)

# Display filtered events
if filtered_events:
    for event in filtered_events:
        st.write(f"### {event['event_title']}")
        st.write(f"**Date**: {event['start_date']}")
        st.write(f"**Time**: {event['start_time']}")
        st.write(f"**Province:{event['province']}")
        st.write(f"**City**: {event['city']}")
        st.write(f"**Ticket Price:{event['price']}")
        st.write(f"**Ticket Price:{event['event_url', 'N/A']}")
        st.write(f"**Description**: {event.get('description', 'No description available')}")
else:
    st.write("No events match your search criteria. Please try different keywords or locations.")
