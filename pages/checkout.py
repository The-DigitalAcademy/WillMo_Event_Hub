import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from establish_connection import connect_to_database

# Function to fetch event details (including price and available tickets)
def fetch_event_details(event_id):
    connection = connect_to_database()
    if connection:
        query = """
            SELECT e.event_id, e.event_title, e.price, e.quantity
            FROM "Events" e
            WHERE e.event_id = %s
        """
        params = [event_id]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchone()
            if data:
                return {
                    "event_id": data[0], 
                    "event_title": data[1], 
                    "price": data[2],
                    "available_quantity": data[3]
                }
    return None

# Function to fetch user details (name, email, etc.) based on email
def fetch_user_details(email):
    connection = connect_to_database()
    if connection:
        query = """
            SELECT name, surname, email
            FROM "Customers"
            WHERE email = %s
        """
        params = [email]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchone()
            if data:
                return {
                    "name": data[0],
                    "surname": data[1],
                    "email": data[2]
                }
    return None

# Checkout page function
def display_checkout_page():
    # Create two columns, one for the title and another for the "Go to Cart" button
    col1, col2 = st.columns([2, 1])

    # Title in the first column
    with col1:
        st.title("Checkout")

    # "Go to Cart" button in the second column
    with col2:
        st.write("")  # Just to align with top right
        if st.button("Go to Cart"):
            switch_page("Cart")

    # Check if user is logged in by checking if email is present in session state
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("You must be signed in to proceed.")
        if st.button("Sign Up"):
            switch_page("Signup")
        return

    # Get user's email from session state (assuming it's saved during login)
    email = st.session_state.get("email", None)
    
    if email:
        # Fetch user details from the database using email
        user_details = fetch_user_details(email)
        if user_details:
            full_name = f"{user_details['name']} {user_details['surname']}"
            st.write(f"**Full Name:** {full_name}")
            st.write(f"**Email:** {user_details['email']}")
        else:
            st.error("User details not found.")
            return
    else:
        st.error("No email found. Please log in.")
        return

    # Get the event details (from session state or DB)
    event_id = st.session_state.get("event_id", None)
    event_details = fetch_event_details(event_id)

    if event_details:
        st.write(f"**Event Title:** {event_details['event_title']}")
        event_price = event_details["price"]
        available_quantity = event_details["available_quantity"]

        if available_quantity > 0:
            # Quantity and price update
            quantity = st.number_input(
                "Select Quantity",
                min_value=1,
                max_value=available_quantity,
                value=1
            )
            price = event_price * quantity
            st.write(f"**Total Price:** R{price}")

            # Layout buttons neatly using columns for the rest
            col1, col2 = st.columns([1, 2])

            # Add to Cart Button in first column
            with col1:
                if st.button("Add to Cart"):
                    # Check if the event already exists in the cart
                    if "cart" not in st.session_state:
                        st.session_state.cart = []

                    event_in_cart = False
                    for item in st.session_state.cart:
                        if item["event_id"] == event_id:
                            if item["quantity"] + quantity > available_quantity:
                                st.error(f"Cannot add {quantity} tickets. Only {available_quantity - item['quantity']} remaining.")
                            else:
                                item["quantity"] += quantity
                                item["total_price"] = item["quantity"] * event_price
                                event_in_cart = True
                                st.success(f"Updated {event_details['event_title']} quantity to {item['quantity']}.")
                            break

                    if not event_in_cart:
                        cart_item = {
                            "event_id": event_id,
                            "event_title": event_details["event_title"],
                            "quantity": quantity,
                            "total_price": price
                        }
                        st.session_state.cart.append(cart_item)
                        st.success(f"Added {event_details['event_title']} to the cart with quantity {quantity}.")
        else:
            st.error("This event is sold out.")
            return

    else:
        st.error("Event details not found.")
        return

    # Back to Event Details Button in second column
    with col2:
        if st.button("Back to Event Details"):
            switch_page("event_details")

# Display checkout page
display_checkout_page()
