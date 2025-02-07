import psycopg2 as ps
import pandas as pd
import streamlit as st
from datetime import datetime

# Database connection
def connect_to_database():
    try:
        connection = ps.connect(
            host='localhost',
            port='5432',
            database='willmo',
            user='postgres',
            password=''
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Fetch data from the database
def fetch_events(connection, query, params):
    try:
        # Use connection.cursor() for psycopg2 and execute the query directly
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Streamlit application
def display_booking_page():

    # Search bar and filters
    with st.container():
        st.subheader("Search and Filter Events")
        search_query = st.text_input("Search events by name:", placeholder="Enter event name")

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_date = st.date_input("Select Date")

        with col2:
            category = st.selectbox(
                "Category",
                ["All", "Charity Event", "Fashion Event", "Festival", "Art Event", "Social Event", "Sports", "Online Event", "Hybrid Event"]
            )

        with col3:
            province = st.selectbox(
                "Province",
                ["All", "Gauteng", "KwaZulu-Natal", "Eastern Cape", "Free State", "Western Cape", "Northern Cape", "North West", "Mpumalanga", "Limpopo"]
            )

    # Fetch and display events
    with st.container():
        connection = connect_to_database()
        if connection:
            query = """
                SELECT e.event_title, e.description, e.start_date, e.start_time, c.category, l.city, l.province 
                FROM "Events" e
                INNER JOIN "Category" c ON e.category_id = c.category_id
                INNER JOIN "Location" l ON e.location_id = l.location_id
                WHERE (%s IS NULL OR e.event_title ILIKE '%%' || %s || '%%')
                AND (%s IS NULL OR e.start_date = %s)
                AND (%s IS NULL OR c.category = %s)
                AND (%s IS NULL OR l.province = %s)
            """

            params = [
                search_query if search_query else None,
                search_query if search_query else None,
                selected_date if selected_date else None,
                selected_date if selected_date else None,
                category if category != "All" else None,
                category if category != "All" else None,
                province if province != "All" else None,
                province if province != "All" else None,
            ]

            events = fetch_events(connection, query, params)

            if not events.empty:
                for _, event in events.iterrows():
                    st.subheader(event['event_title'])
                    st.write(f"**Description:** {event['description']}")
                    st.write(f"**Date:** {event['start_date']} at {event['start_time']}")
                    st.write(f"**Category:** {event['category']}")
                    st.write(f"**Location:** {event['city']}, {event['province']}")
                    st.markdown("---")
            else:
                st.info("No events match your search criteria.")

    # Navigation buttons at the bottom
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Cancel"):
                st.write("Redirecting to homepage...")

        with col2:
            if st.button("Next"):
                st.write("Navigating to the next page...")

# Run the app
display_booking_page()
