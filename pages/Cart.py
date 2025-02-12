import streamlit as st
from event1 import display_booking_page, display_event_details_page
from checkout import display_checkout_page
from establish_connection import connect_to_database

# --- Function to Update Event Quantity ---
def update_event_quantity(event_id, quantity_change):
    connection = connect_to_database()
    if connection:
        query = """UPDATE "Events" SET quantity = quantity + %s WHERE event_id = %s"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (quantity_change, event_id))
                connection.commit()
        except Exception as e:
            st.error(f"Error updating event quantity: {e}")
    else:
        st.error("Database connection failed.")

# --- Function to Check Available Event Quantity ---
def get_event_quantity(event_id):
    connection = connect_to_database()
    if connection:
        query = """SELECT quantity FROM "Events" WHERE event_id = %s"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (event_id,))
                available_quantity = cursor.fetchone()
                return available_quantity[0] if available_quantity else 0
        except Exception as e:
            st.error(f"Error fetching event quantity: {e}")
            return 0
    else:
        st.error("Database connection failed.")
        return 0

# --- Function to Add Event to Cart ---
def add_to_cart(event_id, quantity, event_title, price):
    if "cart" not in st.session_state:
        st.session_state["cart"] = []
    
    # Check if event is already in cart and update its quantity if needed
    event_in_cart = next((item for item in st.session_state["cart"] if item["event_id"] == event_id), None)
    
    # Check if enough tickets are available
    available_quantity = get_event_quantity(event_id)
    if available_quantity < quantity:
        st.error(f"Only {available_quantity} tickets are available for this event.")
        return
    
    if event_in_cart:
        event_in_cart["quantity"] += quantity
        event_in_cart["subtotal"] = event_in_cart["quantity"] * price
    else:
        st.session_state["cart"].append({
            "event_id": event_id,
            "event_title": event_title,
            "quantity": quantity,
            "subtotal": quantity * price
        })
    
    # Update event quantity in the database
    update_event_quantity(event_id, -quantity)  # Decrease available tickets by quantity added to cart
    
    # Update page state
    st.session_state["page"] = "cart"

# --- Display Cart Page ---
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
            st.session_state["page"] = "checkout"

    with col2:
        if st.button("Discard Tickets"):
            confirm_discard = st.radio("Are you sure you want to discard all tickets in the cart?", ("Yes", "No"))
            if confirm_discard == "Yes":
                # Update database: Increase the ticket quantity for each event removed
                for item in st.session_state["cart"]:
                    update_event_quantity(item["event_id"], item["quantity"])  # Restore ticket quantity
                st.session_state["cart"] = []  # Clear the cart
                st.session_state["page"] = "events"

# --- Sidebar Cart Icon ---
def display_cart_icon():
    st.sidebar.markdown("### Your Cart")
    
    # Count the number of items in the cart
    cart_count = sum(item["quantity"] for item in st.session_state.get("cart", []))
    st.sidebar.write(f"🛒 Items in Cart: **{cart_count}**")
    
    # Add a button to navigate to the cart page
    if st.sidebar.button("View Cart"):
        st.session_state["page"] = "cart"

# --- Main Navigation ---
if "page" not in st.session_state:
    st.session_state["page"] = "events"

# Display cart icon in sidebar
display_cart_icon()

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
