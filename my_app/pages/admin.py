import streamlit as st
import psycopg2
from psycopg2 import sql

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_dbname", user="your_username", password="your_password", host="localhost", port="5432"
    )
    return conn

# Function to check if an event exists for the current admin user
def get_event_data_for_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to get event details for the current admin
    cursor.execute(
        sql.SQL("SELECT * FROM events WHERE admin_id = %s"),
        [admin_id]
    )
    
    event_data = cursor.fetchone()  # Fetch one record if it exists
    cursor.close()
    conn.close()
    
    return event_data  # This will return None if no event exists

# Display event details or event creation form
def display_create_event_page(admin_id):
    # Check if event exists for the admin user
    event_data = get_event_data_for_admin(admin_id)
    
    if event_data:
        # If event exists, display event details and stats
        st.markdown("<h3 style='text-align: center;'>Event Details</h3>", unsafe_allow_html=True)
        
        st.write(f"**Event Title:** {event_data[1]}")  # Assuming the event title is in the second column
        st.write(f"**Description:** {event_data[2]}")
        st.write(f"**Category:** {event_data[3]}")
        st.write(f"**Capacity:** {event_data[4]}")
        st.write(f"**Ticket Price:** {event_data[5]} ZAR")
        st.write(f"**Venue Title:** {event_data[6]}")
        st.write(f"**Google Maps Location:** {event_data[7]}")
        st.write(f"**City:** {event_data[8]}")
        st.write(f"**Province:** {event_data[9]}")
        st.write(f"**Start Date:** {event_data[10]}")
        st.write(f"**Start Time:** {event_data[11]}")
        st.write(f"**Event URL:** {event_data[12]}")
        
        # Stats (For example, you could query number of tickets sold, etc.)
        st.write("### Event Stats")
        st.write(f"**Tickets Sold:** {100}")  # Placeholder value, fetch from database if applicable
        st.write(f"**Tickets Available:** {event_data[4] - 100}")  # Assuming total capacity is in event_data[4]
        
    else:
        # If no event exists, prompt the user to create an event
        st.markdown("<h3 style='text-align: center;'>Create Event</h3>", unsafe_allow_html=True)
        
        event_title = st.text_input("Event Title")
        event_description = st.text_area("Event Description")
        
        event_category = st.selectbox(
            "Event Category",
            ["Art Events", "Charity Events", "Fashion Events", "Festival", "Social Events", "Sports Events", "Online", "Hybrid"]
        )
        
        event_capacity = st.number_input("Event Capacity", min_value=1, step=1)
        event_ticket_price = st.number_input("Ticket Price (in ZAR)", min_value=0.0, format="%.2f")
        
        event_venue_title = st.text_input("Venue Title")
        event_google_maps_location = st.text_input("Google Maps Location")
        event_city = st.text_input("City")
        event_province = st.text_input("Province")
        
        event_start_date = st.date_input("Event Start Date") 
        event_start_time = st.time_input("Event Start Time")
        
        event_url = st.text_input("Event URL")
        
        if st.button("Save Event"):
            # Code to save the event to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert event data into the events table (make sure to sanitize inputs)
            cursor.execute(
                sql.SQL("INSERT INTO events (admin_id, event_title, event_description, event_category, event_capacity, event_ticket_price, event_venue_title, event_google_maps_location, event_city, event_province, event_start_date, event_start_time, event_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                [admin_id, event_title, event_description, event_category, event_capacity, event_ticket_price, event_venue_title, event_google_maps_location, event_city, event_province, event_start_date, event_start_time, event_url]
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            # Display a success message
            st.success("Event created successfully!")
            
            # Refresh to show the event details
            st.experimental_rerun()

# Main function to simulate admin login and display page
def main():
    # For the sake of example, let's assume `admin_id` is hardcoded. You should replace this with the actual admin's login/session info.
    admin_id = "your_admin_id"  # This would normally come from user authentication session
    
    display_create_event_page(admin_id)

if __name__ == "__main__":
    main()
