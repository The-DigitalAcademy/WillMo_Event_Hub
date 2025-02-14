import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import psycopg2
import pandas as pd

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
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("You must be signed in to proceed.")
        return

    email = st.session_state.get("email", None)
    if not email:
        st.error("No email found. Please log in.")
        return

    if "cart" not in st.session_state or not st.session_state.cart:
        st.warning("Your cart is empty. Add items before proceeding.")
        return

    # Convert cart data to a DataFrame
    cart_data = pd.DataFrame(st.session_state.cart)

    # Display the cart as a table
    st.subheader("Your Cart")
    st.dataframe(cart_data)

    conn = connect_to_database()
    if not conn:
        st.error("Unable to connect to the database.")
        return

    cursor = conn.cursor()

    try:
        # Step 1: Insert a new booking record into the Bookings table
        cursor.execute(
            'INSERT INTO "Bookings" (email, booking_date, status) VALUES (%s, current_timestamp, %s) RETURNING booking_id',
            (email, 'confirmed')
        )
        # Fetch the booking_id from the returned result
        booking_id_result = cursor.fetchone()
        if booking_id_result:
            booking_id = booking_id_result[0]
        else:
            st.error("Failed to generate booking ID.")
            conn.rollback()
            return

        conn.commit()  # Commit the insertion of the booking

        # Step 2: Iterate over the DataFrame and update the database
        for index, row in cart_data.iterrows():
            event_id = row["event_id"]
            quantity = row["quantity"]

            # Insert into BookingEventMap table
            cursor.execute(
                'INSERT INTO "BookingEventMap" (booking_id, event_id) VALUES (%s, %s)',
                (booking_id, event_id)
            )

            # Check if there are enough tickets available
            cursor.execute(
                'SELECT quantity FROM "Events" WHERE event_id = %s',
                (event_id,)
            )
            available_quantity = cursor.fetchone()[0]

            if available_quantity < quantity:
                st.error(f"Not enough tickets available for event ID {event_id}. Available: {available_quantity}.")
                conn.rollback()  # Rollback if not enough tickets are available
                return

            # Update the Events table to reduce ticket quantity
            cursor.execute(
                'UPDATE "Events" SET quantity = quantity - %s WHERE event_id = %s',
                (quantity, event_id)
            )

        conn.commit()

        # Step 3: Clear the cart
        st.session_state.cart = []

        # Confirmation message
        st.success("Payment processed successfully. Your cart has been cleared.")

        # Redirect to another page if needed
        if st.button("Go to my Profile"):
            switch_page("Profile")

    except Exception as e:
        conn.rollback()
        st.error(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()

# Display the payment page
def display_payment_page():
    st.title("Payment")

    if "cart" in st.session_state and st.session_state.cart:
        st.write("Review your cart and confirm payment.")
        if st.button("Pay Now"):
            process_payment()
    else:
        st.warning("Your cart is empty.")

# Run the display_payment_page function
display_payment_page()
