
import streamlit as st
import pandas as pd
from event1 import display_booking_page
from event1 import display_event_details_page

# --- Page to Display the Checkout Page ---
def display_checkout_page(event_id):
    st.title("Checkout")

    connection = connect_to_database()
    if connection:
        query = """
            SELECT e.event_id, e.event_title, e.image, e.description, e.price, e.quantity, 
                   l.venue_title, l.province, l.city, l.google_maps,
                   c.category, cu.contact, cu.name, cu.surname
            FROM "Events" e
            INNER JOIN "Category" c ON e.category_id = c.category_id
            INNER JOIN "Location" l ON e.location_id = l.location_id
            LEFT JOIN "CustomerMap" cm ON cm.event_id = e.event_id
            LEFT JOIN "Customers" cu ON cu.password = cm.password
            WHERE e.event_id = %s
        """
        params = [event_id]
        event_df = fetch_events(connection, query, params)
        if not event_df.empty:
            event = event_df.iloc[0]
            
            # Display event details
            st.image(event['image'], use_column_width=True)
            st.header(event['event_title'])
            st.subheader("Description")
            st.write(event['description'])
            st.subheader("Location Details")
            st.write(f"**Venue:** {event['venue_title']}")
            st.write(f"**City:** {event['city']}")
            st.write(f"**Province:** {event['province']}")
            st.write(f"**Google Maps:** [View Location]({event['google_maps']})")
            
            # Ticket purchase form
            st.subheader("Purchase Tickets")
            with st.form("checkout_form"):
                quantity = st.number_input(
                    "Number of Tickets", min_value=1, max_value=event['quantity'], value=1
                )
                subtotal = quantity * event['price']
                st.write(f"**Subtotal:** R{subtotal:.2f}")
                
                full_name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email", placeholder="Enter your email")
                phone = st.text_input("Phone Number", placeholder="Enter your phone number")
                
                confirm_button = st.form_submit_button("Confirm Purchase")

                if confirm_button:
                    # Here you would insert booking details into the database
                    st.success(f"Thank you, {full_name}! Your purchase of {quantity} tickets has been confirmed.")
        else:
            st.error("Event not found.")
    else:
        st.error("Could not connect to the database.")

    # Back to events link
    st.markdown('<a href="/" style="text-decoration: none;">&larr; Back to Events</a>', unsafe_allow_html=True)

# --- Main Navigation: Switch Between Pages Based on Query Parameters ---
query_params = st.query_params

if "checkout" in query_params and "event_id" in query_params:
    display_checkout_page(query_params["event_id"][0])
elif "booking" in query_params and "event_id" in query_params:
    display_booking_confirmation_page(query_params["event_id"][0])
elif "event_id" in query_params:
    display_event_details_page(query_params["event_id"][0])
else:
    display_booking_page()
