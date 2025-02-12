import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Function to connect to the PostgreSQL database
def connect_to_database():
    try:
        engine = create_engine("postgresql://your_username:your_password@your_host/your_database")
        conn = engine.raw_connection()
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Fetch user data from the database
def get_user_data(email):
    conn = connect_to_database()
    if conn:
        try:
            query = "SELECT * FROM users WHERE email = %s"
            df = pd.read_sql(query, conn, params=(email,))
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching user data: {e}")
            return None

# Fetch created events from the database
def get_created_events(email):
    conn = connect_to_database()
    if conn:
        try:
            query = "SELECT * FROM events WHERE email = %s"
            df = pd.read_sql(query, conn, params=(email,))
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching created events: {e}")
            return None

# Fetch booking history from the database
def get_booking_history(email):
    conn = connect_to_database()
    if conn:
        try:
            query = "SELECT * FROM bookings WHERE email = %s"
            df = pd.read_sql(query, conn, params=(email,))
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching booking history: {e}")
            return None

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Login Form
if not st.session_state.logged_in:
    st.subheader("Please Sign In or Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user_data = get_user_data(email)
        if user_data is not None and not user_data.empty:
            if user_data.iloc[0]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"Welcome {user_data.iloc[0]['name']} {user_data.iloc[0]['surname']}")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        else:
            st.error("User not found. Please register.")

else:
    user_data = get_user_data(st.session_state.user_email)
    
    if user_data is None or user_data.empty:
        st.error("Error loading profile data.")
        st.stop()

    user = user_data.iloc[0]

    # Display User Profile
    st.title("User Profile")
    st.image(user["image"], width=150)
    st.subheader(f"{user['name']} {user['surname']}")
    st.write(f"📧 Email: {user['email']}")
    st.write(f"📞 Contact: {user['contact']}")
    st.write(f"📍 Location: {user['city']}, {user['province']}")

    # Display Created Events
    created_events = get_created_events(user["email"])
    if created_events is not None and not created_events.empty:
        st.subheader("Your Created Events")
        for _, event in created_events.iterrows():
            st.markdown(f"### {event['event_title']}")
            st.write(f"📍 Venue: {event['venue_title']} ({event['googlec_maps']})")
            st.write(f"📅 Date: {event['start_date']} at {event['start_time']}")
            st.write(f"💵 Price: R{event['price']}")
            st.write(f"🎟 Tickets Sold: {event['quantity']} / {event['capacity']}")
            st.image(event["image"], width=300)
            st.markdown(f"[View Event]({event['event_url']})" if event["event_url"] else "")

    else:
        st.info("No events created yet.")

    # Display Booking History
    booked_events = get_booking_history(user["email"])
    if booked_events is not None and not booked_events.empty:
        st.subheader("Your Ticket History")
        for _, event in booked_events.iterrows():
            st.markdown(f"### {event['event_title']}")
            st.write(f"📅 Booked on: {event['booking_date']}")
            st.write(f"📍 Venue: {event['venue_title']}")
            st.image(event["image"], width=300)
    else:
        st.info("No ticket bookings found.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()
