import psycopg2 as ps
import pandas as pd
import streamlit as st
from datetime import datetime

# Connect to the PostgreSQL database server
conn = ps.connect(host='localhost',
                  port='5432',
                  database='willmo',
                  user='postgres',
                  password='')

# Create cursor to interact with the database
cur = conn.cursor()

# Function to fetch events from the database based on search and filter parameters
def fetch_events(event_name=None, province=None, city=None, category=None, selected_date=None):
    query = """
    SELECT e.event_title, e.start_date, e.start_time, e.description, l.province, l.city, c.category
    FROM Events e
    JOIN Location l ON e.location_id = l.location_id
    JOIN Category c ON e.category_id = c.category_id
    WHERE TRUE
    """
    
    # Adding conditions to the query dynamically based on input
    if event_name:
        query += f" AND e.event_title ILIKE '%{event_name}%'"
    if province:
        query += f" AND l.province = '{province}'"
    if city:
        query += f" AND l.city = '{city}'"
    if category:
        query += f" AND c.category = '{category}'"
    if selected_date:
        query += f" AND e.start_date = '{selected_date}'"

    query += " ORDER BY e.start_date, e.start_time;"
    
    # Execute query and fetch results
    cur.execute(query)
    events = cur.fetchall()
    
    # If no events found for the selected date, return a message
    if not events and selected_date:
        return "No events at this present time."
    
    return events

# Streamlit UI components

# Title
st.title("Event Search & Filter")

# Search bar
event_name = st.text_input("Search Events by Name")

# Filter aside
st.sidebar.header("Filters")

# Dropdowns for filtering
province_options = ['All'] + ['Gauteng', 'KwaZulu-Natal', 'Eastern Cape', 'Free State', 'Western Cape', 'Northern Cape', 'North West', 'Mpumalanga', 'Limpopo']
province = st.sidebar.selectbox("Select Province", province_options)

city = None
if province != 'All':
    city = st.sidebar.text_input("City")

# Category dropdown
category_options = ['All', 'Charity Event', 'Fashion Event', 'Festival', 'Art Event', 'Social Event', 'Sports', 'Online Event', 'Hybrid']
category = st.sidebar.selectbox("Select Category", category_options)

# Date picker for date filtering
selected_date = st.sidebar.date_input("Select Date", min_value=datetime.today())

# Fetch and display events based on filters
if selected_date:
    events = fetch_events(event_name, province if province != 'All' else None, city, category if category != 'All' else None, selected_date)
    if isinstance(events, str):  # If no events are found
        st.write(events)
    else:
        event_df = pd.DataFrame(events, columns=["Event Title", "Start Date", "Start Time", "Description", "Province", "City", "Category"])
        st.write(event_df)
else:
    st.write("Please select a date.")

# Bottom buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Cancel"):
        st.write("Redirecting to Homepage...")  # Placeholder for homepage redirection
        # Implement homepage redirection or other desired action here
with col2:
    if st.button("Next"):
        st.write("Proceeding to next page...")  # Placeholder for next page action
        # Implement action to go to the next page here
