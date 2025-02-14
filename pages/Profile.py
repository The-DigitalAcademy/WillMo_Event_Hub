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
            password=''  # Avoid hardcoding credentials in the script
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        switch_page("Signup")  # Redirect to login page if not logged in

# Function to fetch user data and booked events
def get_user_data_and_events(email):
    connection = connect_to_database()
    if not connection:
        return None, None

    with connection.cursor() as cursor:
        # Fetch user information
        cursor.execute('SELECT * FROM "Customers" WHERE email = %s', (email,))
        user_data = cursor.fetchone()

        if user_data:
            # Fetch booked events for the user
            cursor.execute("""
                SELECT e.event_title, e.start_date, e.start_time, e.description, l.venue_title, l.city, l.province
                FROM "Events" e
                JOIN "Bookings" b ON e.event_id = b.event_id
                JOIN "Location" l ON e.location_id = l.location_id
                WHERE b.email = %s
            """, (email,))
            booked_events = cursor.fetchall()

            # Debugging: Log the booked events
            st.write(f"Booked Events (for email: {email}): {booked_events}")

            return user_data, booked_events
        else:
            return None, None

# Function to update user details
def update_user_details(email, contact, name):
    connection = connect_to_database()
    if not connection:
        st.error("Database connection failed.")
        return

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE "Customers"
            SET contact = %s, name = %s
            WHERE email = %s
        """, (contact, name, email))
        connection.commit()

# Function to log out the user
def logout():
    # Clear session state and redirect to login page
    del st.session_state["logged_in"]
    del st.session_state["email"]
    st.success("You have been logged out successfully!")
    switch_page("Signup")

# Display profile page
def display_profile_page():
    check_logged_in()

    user_email = st.session_state.get("email", "")
    user_data, booked_events = get_user_data_and_events(user_email)

    if user_data:
        contact, name, surname, email = user_data[0], user_data[1], user_data[2], user_data[3]

        # Display user information
        st.write(f"### Profile Information")
        st.write(f"**Name**: {name} {surname}")
        st.write(f"**Contact**: {contact}")
        st.write(f"**Email**: {email}")

        # Display booked events
        st.write("### Your Booked Events")
        if booked_events:
            for event in booked_events:
                st.write(f"### {event[0]}")
                st.write(f"Date: {event[1]} at {event[2]}")
                st.write(f"Location: {event[4]}, {event[5]}, {event[6]}")
                st.write(f"Description: {event[3]}")
        else:
            st.write("No events booked. Browse events and book your tickets!")

        # Form to update name and contact
        st.write("### Update Your Information")
        new_name = st.text_input("Name", value=name)
        new_contact = st.text_input("Contact", value=contact)

        update_button = st.button("Update Information")

        if update_button:
            if new_name != name or new_contact != contact:
                update_user_details(email, new_contact, new_name)
                st.success("Your details have been updated successfully!")
            else:
                st.warning("No changes were made.")
        
        # Logout button
        if st.button("Logout"):
            logout()

    else:
        st.error("User data not found. Please try logging in again.")

# Call the function to display profile page
display_profile_page()
