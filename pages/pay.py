import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import psycopg2

# Function to connect to the database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='willmo',  # Replace with your actual database name
            user='postgres',     # Replace with your PostgreSQL username
            password='Will'      # Replace with your PostgreSQL password
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to process the payment and update the booking
def process_payment():
    # Ensure user is logged in
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("You must be signed in to proceed.")
        return

    email = st.session_state.get("email", None)
    if not email:
        st.error("No email found. Please log in.")
        return

    conn = connect_to_database()
    if not conn:
        st.error("Unable to connect to the database.")
        return

    cursor = conn.cursor()

    try:
        # Insert a new booking record into the Bookings table
        cursor.execute(
            'INSERT INTO "Bookings" (email, booking_date, status) VALUES (%s, current_timestamp, %s) RETURNING booking_id',
            (email, 'confirmed')
        )
        booking_id = cursor.fetchone()[0]  # Retrieve the booking_id after insertion
        conn.commit()

        st.success("Payment successful! Your booking has been confirmed.")

        # Debug: Print the cart to check the event_ids
        st.write("Cart:", st.session_state.cart)

        # Insert records into the BookingEventMap table for each event in the cart
        if "cart" in st.session_state and st.session_state.cart:
            for item in st.session_state.cart:
                event_id = item.get("event_id")  # Get the event_id from the cart
                if event_id is None:
                    st.error("Event ID is missing from the cart item.")
                    return

                # Debug: Print each event_id before inserting
                st.write(f"Inserting event_id: {event_id} for booking_id: {booking_id}")

                cursor.execute(
                    'INSERT INTO "BookingEventMap" (booking_id, event_id) VALUES (%s, %s)',
                    (booking_id, event_id)
                )
            conn.commit()

        # Optionally, clear the cart after booking
        st.session_state.cart = []

        # Optionally, redirect to another page, e.g., confirmation page
        if st.button("Go to my Profile"):
            switch_page("Profile")

    except Exception as e:
        conn.rollback()  # Rollback if there's an error
        st.error(f"An error occurred while processing the payment: {e}")

    finally:
        cursor.close()
        conn.close()

# Display the payment page
def display_payment_page():
    st.title("Payment")

    # Payment Success Message
    st.write("You are about to complete your payment. Click below to confirm your booking.")

    if st.button("Pay Now"):
        process_payment()

# Run the display_payment_page function
display_payment_page()
