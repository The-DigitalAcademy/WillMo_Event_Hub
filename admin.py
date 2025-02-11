import streamlit as st
import psycopg2
from establish_connection import connect_to_database
import pandas as pd

def fetch_event_data(event_id):
    """Fetch event data for the given event ID directly from the Events table."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT event_title, capacity, price, start_date, start_time, description, event_url
                FROM "Events"
                WHERE event_id = %s
            """
            cursor.execute(query, (event_id,))
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

    # Assuming the logged-in user has event_id = 1
    event_id = 1

    # Fetch event data for the specific event ID
    event_data = fetch_event_data(event_id)

    if not event_data:
        st.warning("No events found for this user. Please create an event first.")
        if st.button("Go to Event Creation Page"):
            st.session_state.query_params = {"page": "create_event"}
    else:
        # Convert data to DataFrame for display
        event_df = pd.DataFrame(event_data, columns=[
            "Event Title", "Capacity", "Price (ZAR)", "Start Date", "Start Time", "Description", "Event URL"
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
