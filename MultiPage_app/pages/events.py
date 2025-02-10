import streamlit as st
import psycopg2 as ps
from datetime import datetime

# Database connection function
def fetch_events():
    """Fetch upcoming events from the database."""
    try:
        # Connect to PostgreSQL
        connections = ps.connect(host='localhost',
                          port='5432',
                          database='willmo',
                          user= 'postgres',
                          password= '')
        cursor = connections.cursor()

        # Fetch events from today onward
        query = """
        SELECT event_title, start_date, start_time, venue_title, city, province, description, event_url
        FROM events
        WHERE start_date >= %s
        ORDER BY start_date;
        """
        cursor.execute(query, (datetime.today().strftime("%Y-%m-%d"),))
        events = cursor.fetchall()

        cursor.close()
        connections.close()

        return events

    except Exception as e:
        st.error(f"Error fetching events: {e}")
        return []

# Display events in the Streamlit app
def display_events(events):
    if events:
        for event in events:
            title, date, time, venue, city, province, description, url = event
            st.subheader(title)
            st.write(f"📅 {date} at ⏰ {time}")
            st.write(f"📍 {venue}, {city}, {province}")
            st.write(f"📝 {description}")
            if url:
                st.markdown(f"[More Info]({url})")
            st.write("---")
    else:
        st.info("No upcoming events available.")

# Main function
def main():
    st.title("Upcoming Events")
    events = fetch_events()
    display_events(events)

if __name__ == "__main__":
    main()
