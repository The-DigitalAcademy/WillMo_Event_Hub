import streamlit as st
from datetime import datetime
from pages.events import get_upcoming_events

image_path = "/Users/tshmacm1172/Downloads/WillMo.jpg"
st.image(image_path, width=290)
#st.set_page_config(page_title="Willcome to WillMo Events", page_icon="🧊", layout="wide")

st.title("WillMo Events Hub")


# Search for an event by title and location
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

# Text input for event title
event_title_search = st.text_input("Search by event title", "")
# Select box for location filter (you can add more locations as needed)

location_search = st.selectbox("Filter by location", south_african_cities)

#  Empty events section with a placeholder for now
st.subheader("Upcoming Events")

# Fetch events from events.py
events = get_upcoming_events()

filtered_events = []

for event in events:
    # Check if event title matches the search or if location matches the selected filter
    title_match = event_title_search.lower() in event['title'].lower() if event_title_search else True
    location_match = location_search == "All Locations" or location_search in event['location']
    
    if title_match and location_match:
        filtered_events.append(event)

# Display the filtered events
if filtered_events:
    for event in filtered_events:
        st.write(f"### {event['title']}")
        st.write(f"**Date**: {event['date']}")
        st.write(f"**Location**: {event['location']}")
        st.write(f"**Description**: {event['description']}")
        st.write("---")
else:
    st.write("No events match your search criteria. Please try different keywords or locations.")