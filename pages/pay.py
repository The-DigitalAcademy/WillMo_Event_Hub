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

    # Display cart items in a more detailed and user-friendly way
    st.subheader("Review Your Cart")

    total_cart_price = 0

    conn = connect_to_database()
    cursor = conn.cursor()

    for item in st.session_state.cart:
        event_id = item.get("event_id")
        quantity = item.get("quantity", 1)

        # Fetch event details, including price, from the database
        cursor.execute(
            'SELECT event_title, image, price FROM "Events" WHERE event_id = %s',
            (event_id,),
        )
        event_details = cursor.fetchone()

        if event_details:
            event_title, event_image, price = event_details
            total_price = quantity * price
        else:
            event_title, event_image, price, total_price = "Unknown Event", None, 0, 0

        st.write(f"**Event Title**: {event_title}")
        st.write(f"**Quantity**: {quantity}")
        st.write(f"**Price per Ticket**: R{price}")
        st.write(f"**Total Price**: R{total_price}")

        if event_image:
            st.image(event_image, width=150)

        st.markdown("---")
        total_cart_price += total_price

    st.write(f"**Total Cart Price**: R{total_cart_price}")

    # Handle the booking and payment process
    try:
        cursor.execute(
            'INSERT INTO "Bookings" (email, booking_date, status) VALUES (%s, current_timestamp, %s) RETURNING booking_id',
            (email, 'pending')  # Status is set to 'pending' initially
        )
        booking_id_result = cursor.fetchone()
        if booking_id_result:
            booking_id = booking_id_result[0]
        else:
            st.error("Failed to generate booking ID.")
            conn.rollback()
            return

        conn.commit()  # Commit the insertion of the booking

        for item in st.session_state.cart:
            event_id = item["event_id"]
            quantity = item["quantity"]

            cursor.execute(
                'INSERT INTO "BookingEventMap" (booking_id, event_id) VALUES (%s, %s)',
                (booking_id, event_id)
            )

            cursor.execute(
                'SELECT quantity FROM "Events" WHERE event_id = %s',
                (event_id,)
            )
            available_quantity = cursor.fetchone()[0]

            if available_quantity < quantity:
                st.error(f"Not enough tickets available for event ID {event_id}. Available: {available_quantity}.")
                conn.rollback()
                return

            cursor.execute(
                'UPDATE "Events" SET quantity = quantity - %s WHERE event_id = %s',
                (quantity, event_id)
            )

        # Change the booking status to 'confirmed' after payment is successful
        cursor.execute(
            'UPDATE "Bookings" SET status = %s WHERE booking_id = %s',
            ('confirmed', booking_id)
        )
        conn.commit()

        # Clear the cart
        st.session_state.cart = []

        st.success("Payment processed successfully. Your cart has been cleared.")
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
