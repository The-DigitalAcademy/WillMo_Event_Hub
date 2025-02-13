import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import psycopg2

# Function to connect to the database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='willmo',  # Update this with your actual database name
            user='postgres',     # Update this with your actual PostgreSQL username
            password='Will'      # Update this with your actual PostgreSQL password
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")

# Function to display cart with a better layout
def display_cart():
    st.title("Your Cart")

    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Check if the cart is in the session state and has items
    if "cart" in st.session_state and st.session_state.cart:
        cart = st.session_state.cart
        total_cart_price = 0  # Keep track of the total price

        for i, item in enumerate(cart):
            event_id = item.get('event_id')

            # Fetch event details from the database
            cursor.execute("SELECT event_title, image, price FROM Events WHERE event_id = %s", (event_id,))
            event_details = cursor.fetchone()

            if event_details:
                event_title, event_image, price = event_details
            else:
                event_title, event_image, price = "Unknown Event", None, 0

            quantity = item.get('quantity', 1)
            total_price = price * quantity

            with st.expander(f"Event: {event_title}"):  # Use expander for each item to show details
                # Show the event details
                if event_image:
                    st.image(event_image, use_column_width=True)  # Display event image
                st.write(f"**Quantity**: {quantity}")
                st.write(f"**Price per Ticket**: R{price}")
                st.write(f"**Total Price**: R{total_price}")

                # Add a remove button for each item in the cart
                if st.button(f"Remove Event {event_title}", key=f"remove_{i}"):
                    # Remove item from cart and update the database
                    st.session_state.cart.pop(i)
                    cursor.execute(
                        "DELETE FROM Cart WHERE email = %s AND event_id = %s",
                        (st.session_state.user_email, item['event_id'])
                    )
                    conn.commit()  # Commit changes to the database
                    st.success(f"Removed {event_title} from the cart.")
                    st.experimental_rerun()  # Use rerun to refresh the page

                total_cart_price += total_price  # Add to the total cart price

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

# Display Cart
display_cart()
