import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import psycopg2
import os
from establish_connection import connect_to_database

# Function to handle event images
def display_event_image(image_path, event_title):
    if image_path:
        if image_path.startswith("http"):
            st.image(image_path, caption=event_title, use_container_width=False, width=150)
        else:
            local_image_path = os.path.join(os.getcwd(), image_path.lstrip("/"))
            if os.path.exists(local_image_path):
                st.image(local_image_path, caption=event_title, use_container_width=False, width=150)
            else:
                st.warning(f"⚠️ Image not found: {local_image_path}")
    else:
        st.warning("⚠️ No image available for this event.")

# Function to check if the user is logged in
def check_logged_in():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.error("No email found in session. Please log in again.")
        switch_page("Signup")

# Function to display the cart
def display_cart():
    check_logged_in()

    st.title("Your Cart")

    conn = connect_to_database()
    if not conn:
        st.error("Unable to connect to the database. Please try again later.")
        return

    cursor = conn.cursor()

    if "cart" in st.session_state and st.session_state.cart:
        cart = st.session_state.cart
        total_cart_price = 0

        for i, item in enumerate(cart):
            event_id = item.get('event_id')

            try:
                cursor.execute(
                    'SELECT event_title, image, price, quantity FROM "Events" WHERE event_id = %s',
                    (event_id,)
                )
                event_details = cursor.fetchone()

                if event_details:
                    event_title, event_image, price, available_quantity = event_details
                else:
                    event_title, event_image, price, available_quantity = "Unknown Event", None, 0, 0

                with st.expander(f"Event: {event_title}", expanded=False):
                    display_event_image(event_image, event_title)

                    current_quantity = item.get("quantity", 1)
                    new_quantity = st.number_input(
                        f"Quantity for {event_title}",
                        min_value=1,
                        max_value=available_quantity,
                        value=current_quantity,
                        key=f"quantity_{i}"
                    )

                    if new_quantity != current_quantity:
                        if new_quantity <= available_quantity:
                            st.session_state.cart[i]["quantity"] = new_quantity
                            st.session_state.cart[i]["total_price"] = new_quantity * price

                            try:
                                cursor.execute(
                                    'UPDATE "Cart" SET cart_quantity = %s WHERE email = %s AND event_id = %s',
                                    (new_quantity, st.session_state.get("email", ""), event_id)
                                )
                                conn.commit()
                                st.success(f"Updated quantity for {event_title} to {new_quantity}.")
                            except Exception as e:
                                st.error(f"Error updating quantity in database: {e}")
                        else:
                            st.error(f"Cannot update to {new_quantity} tickets. Only {available_quantity} remaining.")

                    total_price = new_quantity * price
                    st.write(f"**Price per Ticket**: R{price}")
                    st.write(f"**Total Price**: R{total_price}")

                    if st.button(f"Remove {event_title}", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)

                        try:
                            cursor.execute(
                                'DELETE FROM "Cart" WHERE email = %s AND event_id = %s',
                                (st.session_state.get("email", ""), event_id)
                            )
                            conn.commit()
                            st.success(f"Removed {event_title} from the cart.")
                        except Exception as e:
                            st.error(f"Error deleting item from database: {e}")

                total_cart_price += total_price

            except psycopg2.Error as e:
                conn.rollback()
                st.error(f"Error fetching details for event ID {event_id}: {e}")
                continue

        st.write(f"**Total Cart Price**: R{total_cart_price}")

    else:
        st.write("Your cart is empty.")

    if st.button("Pay Now"):
        switch_page("pay")

    cursor.close()
    conn.close()


display_cart()