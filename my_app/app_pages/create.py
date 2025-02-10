import streamlit as st

def create():
    # Initialize session state for values if not already set
    initialize_session_state()

    st.markdown("<h3 style='text-align: center;'>Create Event</h3>", unsafe_allow_html=True)
    st.write("Here you can create new events.")

    # Event creation form
    event_title = st.text_input("Event Title", value=st.session_state["event_title"], help="Enter a suitable title for your event.", key="event_title")
    event_description = st.text_area("Event Description", value=st.session_state["event_description"], help="Describe the event in detail.", key="event_description")
    event_category = st.selectbox(
        "Event Category",
        ["Art Events", "Charity Events", "Fashion Events", "Festival", "Social Events", "Sports Events", "Online", "Hybrid"],
        index=["Art Events", "Charity Events", "Fashion Events", "Festival", "Social Events", "Sports Events", "Online", "Hybrid"].index(st.session_state["event_category"]),
        key="event_category"
    )

    # Event-specific details
    event_capacity = st.number_input("Event Capacity", min_value=1, value=st.session_state["event_capacity"], step=1, key="event_capacity")
    event_ticket_price = st.number_input("Ticket Price (in ZAR)", min_value=0.0, value=st.session_state["event_ticket_price"], format="%.2f", key="event_ticket_price")

    # Venue and location for physical events
    event_venue_title = st.text_input("Venue Title") if event_category != "Online" else "N/A"
    event_google_maps_location = st.text_input("Google Maps Location") if event_category != "Online" else "N/A"
    event_city = st.text_input("City") if event_category != "Online" else "N/A"
    event_province = st.text_input("Province") if event_category != "Online" else "N/A"

    event_start_date = st.date_input("Event Start Date", key="event_start_date")
    event_start_time = st.time_input("Event Start Time", key="event_start_time")

    event_url = st.text_input("Event URL") if event_category in ["Online", "Hybrid"] else "N/A"

    # Validation check before proceeding
    if st.button("Next"):
        if not event_title or not event_description or not event_start_date or not event_start_time:
            st.error("Please fill in all required fields (Title, Description, Date, Time) to proceed.")
        else:
            # Save event details to session state
            st.session_state.update({
                "event_title": event_title,
                "event_description": event_description,
                "event_category": event_category,
                "event_capacity": event_capacity,
                "event_ticket_price": event_ticket_price,
                "event_venue_title": event_venue_title,
                "event_google_maps_location": event_google_maps_location,
                "event_city": event_city,
                "event_province": event_province,
                "event_start_date": event_start_date,
                "event_start_time": event_start_time,
                "event_url": event_url,
            })
            # Move to next page (without direct widget modification after rendering)
            st.session_state.page = "upload_picture"
            st.experimental_rerun()
