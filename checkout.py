
import streamlit as st
from event1 import connect_to_database, fetch_events, display_booking_page, display_event_details_page

def display_checkout_page():
    event_id = st.session_state.get("event_id")
    if not event_id:
        st.error("No event selected.")
        return

    # Fetch event details for checkout page
    connection = connect_to_database()
    if connection:
        query = """
            SELECT e.event_id, e.event_title, e.image, e.description, e.price, e.quantity, 
                   l.venue_title, l.province, l.city, l.google_maps
            FROM "Events" e
            INNER JOIN "Location" l ON e.location_id = l.location_id
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
            
            # Quantity input
            quantity = st.number_input("Quantity", min_value=1, max_value=event['quantity'], value=1)

            # Calculate subtotal
            price = event['price']
            subtotal = price * quantity
            st.write(f"**Price per Ticket:** R{price}")
            st.write(f"**Subtotal:** R{subtotal}")

            # Add to Cart button
            if st.button("Add to Cart"):
                if "cart" not in st.session_state:
                    st.session_state["cart"] = []
                
                # Add event to cart
                st.session_state["cart"].append({
                    "event_id": event['event_id'],
                    "event_title": event['event_title'],
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal
                })
                st.success(f"Added {event['event_title']} (x{quantity}) to cart!")
        else:
            st.error("Event not found.")
    else:
        st.error("Could not connect to the database.")

    # Back link
    st.markdown('<a href="/" style="text-decoration: none;">&larr; Back to Events</a>', unsafe_allow_html=True)