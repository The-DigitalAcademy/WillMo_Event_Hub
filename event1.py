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
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchall()
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
            else:
                columns = []
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame(columns=columns)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Streamlit application
def display_booking_page():
    st.title("Event Finder")

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
                ["All", "Charity Event", "Fashion Event", "Festival", "Art Event", "Social Event", "Sports", "Online Event", "Hybrid"]
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
            # Constructing the query dynamically based on selected filters
            query = """
                SELECT e.event_title, e.description, e.start_date, e.start_time, c.category, l.city, l.province 
                FROM "Events" e
                INNER JOIN "Category" c ON e.category_id = c.category_id
                INNER JOIN "Location" l ON e.location_id = l.location_id
                WHERE 1=1
            """

            params = []

            # Add conditions based on filters
            if search_query:
                query += " AND e.event_title ILIKE %s"
                params.append(f"%{search_query}%")
            if selected_date:
                query += " AND e.start_date = %s"
                params.append(selected_date)
            if category != "All":
                query += " AND c.category = %s"
                params.append(category)
            if province != "All":
                query += " AND l.province = %s"
                params.append(province)

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
        col1, col2, _ = st.columns([1, 1, 6])

        with col1:
            if st.button("Cancel"):
                st.write("Redirecting to homepage...")

        with col2:
            if st.button("Next"):
                st.write("Navigating to the next page...")

# Run the app
display_booking_page()
