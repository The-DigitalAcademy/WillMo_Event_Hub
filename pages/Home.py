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
            SELECT  e.image, l.province, l.city, e.description, e.price, e.quantity, e.event_url
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
st.markdown("""
        <style>
        .event-card {
            border: 1px solid #ccc;
            padding: 16px;
            margin: 10px;
            border-radius: 8px;
            width: 400px;
            height: 500px;
        }
        .event-card img {
            max-height: 200px;
            margin-bottom: 10px;
        }
        .event-card h3 {
            font-size: 1.2em;
            margin-bottom: 8px;
        }
        .event-card p {
            font-size: 1em;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

if filtered_events:
    cols = st.columns(3)  # Create 3 columns for each row
    for idx, event in enumerate(filtered_events):
        col = cols[idx % 3]  # Cycle through columns
        with col:
            st.markdown(f"""
                                <div class="event-card">
                                    <img src="{event['image']}" alt="Event Image">
                                    <h3>{event['event_title']}</h3>
                                    <p><strong>Date:</strong> {event['start_date']}</p>
                                    <p><strong>Time:</strong> {event['start_time']}</p>
                                    <p><strong>Location:</strong> {event['city']}, {event['province']}</p>
                                    <p><strong>Price:</strong> R{event['price']}</p>
                                    <p><strong>Available Tickets:</strong> {event['quantity']} </p>
                                </div>
                            </a>
                        """, unsafe_allow_html=True)
else:
    st.write("No events match your search criteria. Please try different keywords or locations.")
