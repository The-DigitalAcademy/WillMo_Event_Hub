import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Fetch user details (Placeholder for now)
def get_user_details():
    # For simplicity, we're using static data here
    return {"user_id": 1, "name": "John Doe", "email": "johndoe@example.com"}

# Checkout page function
def display_checkout_page():
    st.title("Checkout")

    # Get user details
    user_details = get_user_details()
    st.write(f"**User:** {user_details['name']}")
    st.write(f"**Email:** {user_details['email']}")

    # Quantity and price update
    event_id = st.session_state.get("event_id", None)
    event_price = 100  # Example static price
    quantity = st.number_input("Select Quantity", min_value=1, max_value=10, value=1)

    price = event_price * quantity
    st.write(f"**Total Price:** R{price}")

    if st.button("Add to Cart"):
        # Add event and quantity to the cart
        cart_item = {"event_id": event_id, "quantity": quantity, "total_price": price}
        if "cart" not in st.session_state:
            st.session_state.cart = []
        st.session_state.cart.append(cart_item)
        st.write("Item added to cart.")

    if st.button("Go to Cart"):
        switch_page("Cart")

# Display checkout page
display_checkout_page()
