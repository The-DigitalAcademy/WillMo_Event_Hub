import streamlit as st
import psycopg2 as ps
from streamlit_extras.switch_page_button import switch_page

# Function to connect to the PostgreSQL database server
def connect_to_database():
    try:
        connection = ps.connect(
            host='localhost',
            port='5432',
            database='willmo',
            user='postgres',
            password='Will'  # Avoid hardcoding credentials in the script
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        switch_page("Signup")  # Redirect to login page if not logged in

# Function to fetch user data and their events
def get_user_data_and_events(email):
    connection = connect_to_database()
    if not connection:
        return None, None, None

    with connection.cursor() as cursor:
        # Fetch user information
        cursor.execute('SELECT * FROM "Customers" WHERE email = %s', (email,))
        user_data = cursor.fetchone()

        # Fetch user's created events (if they are an organizer)
        cursor.execute('''
            SELECT e.event_id, e.event_title, e.start_date, e.start_time, e.description, 
                   l.venue_title, l.city, l.province, e.price, e.quantity
            FROM "Events" e
            JOIN "Organizer" o ON e.organizer_id = o.organizer_id
            JOIN "Location" l ON e.location_id = l.location_id
            WHERE o.email = %s
        ''', (email,))
        created_events = cursor.fetchall()

        # Fetch ticket sales and profit
        event_sales = {}
        for event in created_events:
            event_id = event[0]
            cursor.execute('''
                SELECT COUNT(*), SUM(e.price) FROM "Bookings" b
                JOIN "Events" e ON b.event_id = e.event_id
                WHERE b.event_id = %s AND b.status = 'confirmed'
            ''', (event_id,))
            sales_data = cursor.fetchone()
            event_sales[event_id] = sales_data if sales_data else (0, 0.0)

        return user_data, created_events, event_sales

# Function to delete an event
def delete_event(event_id):
    connection = connect_to_database()
    if not connection:
        st.error("Database connection failed.")
        return

    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM "Events" WHERE event_id = %s', (event_id,))
        connection.commit()
        st.success("Event deleted successfully!")

# Display profile page
def display_profile_page():
    check_logged_in()
    
    user_email = st.session_state.get("email", "")
    user_data, created_events, event_sales = get_user_data_and_events(user_email)

    if user_data:
        contact, name, surname, email = user_data[0], user_data[1], user_data[2], user_data[3]

        # Display user information
        st.write(f"### Profile Information")
        st.write(f"**Name**: {name} {surname}")
        st.write(f"**Contact**: {contact}")
        st.write(f"**Email**: {email}")

        # Display created events
        st.write("### Your Created Events")
        if created_events:
            for event in created_events:
                event_id, title, date, time, desc, venue, city, province, price, tickets = event
                sales_count, revenue = event_sales[event_id]
                
                st.write(f"#### {title}")
                st.write(f"Date: {date} at {time}")
                st.write(f"Location: {venue}, {city}, {province}")
                st.write(f"Description: {desc}")
                st.write(f"Ticket Price: ${price}")
                st.write(f"Tickets Sold: {sales_count}/{tickets}")
                st.write(f"Total Revenue: ${revenue}")
                
                # Edit and Delete Buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {title}"):
                        switch_page("Edit_Event")
                with col2:
                    if st.button(f"Delete {title}"):
                        delete_event(event_id)
                        st.experimental_rerun()
        else:
            st.write("No events created. Start organising now!")
    else:
        st.error("User data not found. Please try logging in again.")

# Call the function to display profile page
display_profile_page()
