import streamlit as st
from event1 import display_booking_page

# Initialize session state for cart if not already done
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- Function to Display the Cart ---
def display_cart_page():
    st.title("Your Shopping Cart")

    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty.")
    else:
        total_price = 0
        for index, item in enumerate(st.session_state.cart):
            st.write(f"**{item['event_title']}**")
            subtotal = item['ticket_quantity'] * item['price']
            st.write(f"Tickets: {item['ticket_quantity']} x R{item['price']} = R{subtotal}")
            total_price += subtotal
            # Provide a remove button for each cart item
            if st.button(f"Remove {item['event_title']}", key=f"remove_{item['event_id']}"):
                # Remove item from cart
                st.session_state.cart.pop(index)
                # Re-render the cart page after removal
                st.experimental_rerun()
            st.write("---")
        st.write(f"**Total: R{total_price}**")
        
        if st.button("Proceed to Checkout"):
            st.success("Checkout process not implemented yet!")

    # Back to events link
    st.markdown('<a href="/" style="text-decoration: none;">&larr; Back to Events</a>', unsafe_allow_html=True)

# --- Function to Display Event Booking Page ---
def display_ticket_booking_page(event_id, event_title, event_price):
    st.title("Add Tickets to Cart")
    st.write(f"**Event Title:** {event_title}")
    st.write(f"**Price per Ticket:** R{event_price}")
    ticket_quantity = st.number_input("Number of Tickets", min_value=1, max_value=10, value=1)
    if st.button("Add to Cart"):
        # Add event to the cart
        event_exists = False
        for item in st.session_state.cart:
            if item["event_id"] == event_id:
                item["ticket_quantity"] += ticket_quantity
                event_exists = True
                break
        if not event_exists:
            st.session_state.cart.append({
                "event_id": event_id,
                "event_title": event_title,
                "ticket_quantity": ticket_quantity,
                "price": event_price
            })
        st.success(f"Added {ticket_quantity} ticket(s) for {event_title} to your cart!")
        st.experimental_rerun()

    # Link back to the events page
    st.markdown('<a href="/" style="text-decoration: none;">&larr; Back to Events</a>', unsafe_allow_html=True)

# --- Main Navigation Logic ---

query_params = st.query_params

if "cart" in query_params:
    display_cart_page()
elif "event_id" in query_params and "event_title" in query_params and "event_price" in query_params:
    display_ticket_booking_page(
        event_id=query_params["event_id"][0],
        event_title=query_params["event_title"][0],
        event_price=float(query_params["event_price"][0])
    )
else:
    display_booking_page()

