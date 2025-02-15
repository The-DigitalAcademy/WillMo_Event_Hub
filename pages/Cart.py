import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import psycopg2
import os

# Function to connect to the database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='willmo',  # Update with your actual database name
            user='postgres',     # Update with your PostgreSQL username
            password='Will'      # Update with your PostgreSQL password
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        switch_page("Signup")  # Redirect to login page if not logged in

# Function to display cart
def display_cart():
    check_logged_in()  # Ensure the user is logged in

    st.title("Your Cart")

    # Connect to the database
    conn = connect_to_database()
    if not conn:
        st.error("Unable to connect to the database. Please try again later.")
        return

    cursor = conn.cursor()

    # Check if the cart is in the session state and has items
    if "cart" in st.session_state and st.session_state.cart:
        cart = st.session_state.cart
        total_cart_price = 0  # Keep track of the total price

        for i, item in enumerate(cart):
            event_id = item.get('event_id')

            try:
                # Fetch event details from the database
                cursor.execute(
                    'SELECT event_title, image, price FROM "Events" WHERE event_id = %s',
                    (event_id,)
                )
                event_details = cursor.fetchone()

                if event_details:
                    event_title, event_image, price = event_details
                else:
                    event_title, event_image, price = "Unknown Event", None, 0

                # Handle image path
                event_image_path = os.path.join('event_images', event_image) if event_image else None

                # Display event details
                with st.expander(f"Event: {event_title}", expanded=False):
                    if event_image and os.path.exists(event_image_path):
                        st.image(event_image_path, width=150)  # Smaller event image
                    else:
                        st.error(f"Image not found: {event_image_path}")

                    # Display current quantity and allow updates
                    current_quantity = item.get("quantity", 1)
                    new_quantity = st.number_input(
                        f"Quantity for {event_title}",
                        min_value=1,
                        max_value=10,
                        value=current_quantity,
                        key=f"quantity_{i}"
                    )

                    # If quantity is updated, update the cart and database
                    if new_quantity != current_quantity:
                        st.session_state.cart[i]["quantity"] = new_quantity
                        st.session_state.cart[i]["total_price"] = new_quantity * price

                        # Debug: Print query being executed
                        st.write(f"Updating quantity for event_id {event_id} to {new_quantity}")
                        try:
                            cursor.execute(
                                'UPDATE "Cart" SET cart_quantity = %s WHERE email = %s AND event_id = %s',
                                (new_quantity, st.session_state.get("user_email", ""), event_id)
                            )
                            conn.commit()  # Commit changes to the database
                            st.success(f"Updated quantity for {event_title} to {new_quantity}.")
                        except Exception as e:
                            st.error(f"Error updating quantity in database: {e}")

                    # Show prices
                    total_price = new_quantity * price
                    st.write(f"**Price per Ticket**: R{price}")
                    st.write(f"**Total Price**: R{total_price}")

                    # Add a remove button for each item
                    if st.button(f"Remove {event_title}", key=f"remove_{i}"):
                        # Remove item from cart
                        st.session_state.cart.pop(i)

                        # Debug: Print query being executed
                        st.write(f"Removing item with event_id {event_id}")
                        try:
                            cursor.execute(
                                'DELETE FROM "Cart" WHERE email = %s AND event_id = %s',
                                (st.session_state.get("user_email", ""), event_id)
                            )
                            conn.commit()  # Commit changes to the database
                            st.success(f"Removed {event_title} from the cart.")
                        except Exception as e:
                            st.error(f"Error deleting item from database: {e}")

                        # Refresh the page immediately
                        st.experimental_rerun()

                total_cart_price += total_price  # Add to the total cart price

            except psycopg2.Error as e:
                conn.rollback()  # Rollback transaction on error
                st.error(f"Error fetching details for event ID {event_id}: {e}")
                continue

        # Show the total cart price at the bottom
        st.write(f"**Total Cart Price**: R{total_cart_price}")

    else:
        st.write("Your cart is empty.")

    # Button to proceed to checkout
    if st.button("Pay Now"):
        switch_page("pay")

    # Close connection
    cursor.close()
    conn.close()

# Function to add an event to the cart
def add_to_cart(event_id, event_title, quantity, price):
    if "cart" not in st.session_state:
        st.session_state.cart = []

    conn = connect_to_database()
    if not conn:
        st.error("Unable to connect to the database.")
        return

    cursor = conn.cursor()

    # Check if the event is already in the cart
    for item in st.session_state.cart:
        if item["event_id"] == event_id:
            # Update the quantity and total price if event exists
            item["quantity"] += quantity
            item["total_price"] = item["quantity"] * price

            # Debug: Print query being executed
            st.write(f"Updating quantity for event_id {event_id} to {item['quantity']}")
            try:
                cursor.execute(
                    'UPDATE "Cart" SET cart_quantity = %s WHERE email = %s AND event_id = %s',
                    (item["quantity"], st.session_state.get("user_email", ""), event_id)
                )
                conn.commit()  # Commit changes to the database
                st.success(f"Updated quantity for {event_title}.")
            except Exception as e:
                st.error(f"Error updating quantity in database: {e}")

            cursor.close()
            conn.close()
            return

    # Add new event to the cart
    st.session_state.cart.append({
        "event_id": event_id,
        "event_title": event_title,
        "quantity": quantity,
        "total_price": price * quantity
    })

    # Insert new entry into the database (cart_quantity is the correct field)
    try:
        cursor.execute(
            'INSERT INTO "Cart" (email, event_id, cart_quantity) VALUES (%s, %s, %s)',
            (st.session_state.get("user_email", ""), event_id, quantity)
        )
        conn.commit()  # Commit changes to the database
        st.success(f"Added {event_title} to the cart.")
    except Exception as e:
        st.error(f"Error adding to cart in database: {e}")

    cursor.close()
    conn.close()

# Display Cart
display_cart()
