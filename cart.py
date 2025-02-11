import streamlit as st
from event1 import display_booking_page, display_event_details_page
from checkout import display_checkout_page

def display_cart_page():
    if "cart" not in st.session_state or len(st.session_state["cart"]) == 0:
        st.write("Your cart is empty.")
        return

    st.header("Your Cart")
    
    total = 0
    for item in st.session_state["cart"]:
        st.subheader(item["event_title"])
        st.write(f"**Quantity:** {item['quantity']}")
        st.write(f"**Subtotal:** R{item['subtotal']}")
        total += item["subtotal"]
    
    st.write(f"**Total Price:** R{total}")
    
    # Add buttons for actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Pay Now"):
            st.write("Proceeding to payment...")
            # Redirect to a payment page or other action
            st.session_state["page"] = "payment"
            st.experimental_rerun()

    with col2:
        if st.button("Discard Tickets"):
            st.session_state["cart"] = []  # Clear the cart
            st.write("Your cart has been emptied.")
            st.experimental_rerun()

# --- Main Navigation: Switch Between the Booking, Details, Checkout, and Cart Pages ---

if "page" not in st.session_state:
    st.session_state["page"] = "events"

if st.session_state["page"] == "events":
    query_params = st.query_params
    if "event_id" in query_params:
        st.session_state["event_id"] = query_params["event_id"][0]
        display_event_details_page(query_params["event_id"][0])
    else:
        display_booking_page()
elif st.session_state["page"] == "checkout":
    display_checkout_page()
elif st.session_state["page"] == "cart":
    display_cart_page()