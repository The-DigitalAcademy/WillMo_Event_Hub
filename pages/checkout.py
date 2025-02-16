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

def handle_add_to_cart(event_id, quantity, event_details, available_quantity, email):
    connection = connect_to_database()
    event_in_cart = False

    # Prevent adding to the cart if the quantity exceeds available tickets
    if quantity > available_quantity:
        st.error(f"Cannot add {quantity} tickets. Only {available_quantity} remaining.")
        return  # Don't add to cart if quantity exceeds available tickets

    # Check if the event already exists in the cart
    for item in st.session_state.cart:
        if item["event_id"] == event_id:
            if item["quantity"] + quantity > available_quantity:
                st.error(f"Cannot add {quantity} tickets. Only {available_quantity - item['quantity']} remaining.")
                return  # Stop if adding exceeds available tickets
            else:
                item["quantity"] += quantity
                item["total_price"] = item["quantity"] * event_details["price"]
                event_in_cart = True
                st.success(f"Updated {event_details['event_title']} quantity to {item['quantity']}.")

                # Update the quantity in the database
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE "Cart" 
                    SET cart_quantity = %s 
                    WHERE email = %s AND event_id = %s
                """, (item["quantity"], email, event_id))
                connection.commit()
                st.success(f"Updated {event_details['event_title']} in the database.")
            break

    # If the event is not in the cart, add it if the quantity is valid
    if not event_in_cart:
        if quantity <= available_quantity:
            cart_item = {
                "event_id": event_id,
                "event_title": event_details["event_title"],
                "quantity": quantity,
                "total_price": event_details["price"] * quantity
            }
            st.session_state.cart.append(cart_item)
            st.success(f"Added {event_details['event_title']} to the cart with quantity {quantity}.")

            # Insert new cart item into the database
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO "Cart" (email, event_id, cart_quantity) 
                VALUES (%s, %s, %s)
            """, (email, event_id, quantity))
            connection.commit()

    connection.close()


# Checkout page function
def display_checkout_page():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("Checkout")

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("You must be signed in to proceed.")
        if st.button("Sign Up"):
            switch_page("Signup")
        return

    email = st.session_state.get("email", None)
    
    if email:
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

    event_id = st.session_state.get("event_id", None)
    event_details = fetch_event_details(event_id)

    if event_details:
        st.write(f"**Event Title:** {event_details['event_title']}")
        event_price = event_details["price"]
        available_quantity = event_details["available_quantity"]

        if available_quantity > 0:
            quantity = st.number_input(
                "Select Quantity",
                min_value=1,
                max_value=available_quantity,
                value=1
            )
            price = event_price * quantity
            st.write(f"**Total Price:** R{price}")

            col1, col2 = st.columns([1, 2])

            with col1:
                if st.button("Add to Cart"):
                    if "cart" not in st.session_state:
                        st.session_state.cart = []

                    handle_add_to_cart(event_id, quantity, event_details, available_quantity, email)

            with col2:
                if st.button("Back to Event Details"):
                    switch_page("event_details")
        else:
            st.error("This event is sold out.")
            return

    else:
        st.error("Event details not found.")
        return

# Display checkout page
display_checkout_page()
