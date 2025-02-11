import streamlit as st
import psycopg2
from establish_connection import connect_to_database
import pandas as pd

def fetch_event_data():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT e.event_title, e.capacity, e.price, e.start_date, e.start_time, l.city, l.province
                FROM "Events" e
                JOIN "Location" l ON e.location_id = l.location_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if rows:
                return rows
            return None

        except Exception as e:
            st.error(f"Error fetching event data: {e}")
            return None

    st.error("Database connection failed.")
    return None

def admin_dashboard():
    st.title("Admin Dashboard")

    # Fetch event data
    event_data = fetch_event_data()

    if not event_data:
        st.warning("No events created. Please create an event first.")
        if st.button("Go to Event Creation Page"):
            # Use st.query_params instead of st.experimental_set_query_params
            st.session_state.query_params = {"page": "create_event"}
    else:
        # Convert data to DataFrame for display
        event_df = pd.DataFrame(event_data, columns=[
            "Event Title", "Capacity", "Price (ZAR)", "Start Date", "Start Time", "City", "Province"
        ])

        st.subheader("Event Overview")
        st.dataframe(event_df)

        # Event Statistics
        total_capacity = event_df["Capacity"].sum()
        total_revenue = (event_df["Capacity"] * event_df["Price (ZAR)"]).sum()

        st.metric("Total Capacity", total_capacity)
        st.metric("Potential Revenue (ZAR)", total_revenue)

        st.subheader("Event History")
        st.dataframe(event_df)

if __name__ == "__main__":
    admin_dashboard()
