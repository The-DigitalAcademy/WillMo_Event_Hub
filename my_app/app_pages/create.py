import streamlit as st

# Ensure session state variables are set
if "page" not in st.session_state:
    st.session_state.page = "create"


def create_page():
    st.markdown("<h3 style='text-align: center;'>Create Event</h3>", unsafe_allow_html=True)
    st.write("Here you can create new events.")

    # Event creation form
    event_title = st.text_input("Event Title", help="Enter a suitable title for your event.")
    event_description = st.text_area("Event Description", help="Describe the event in detail.")
    event_category = st.selectbox(
        "Event Category",
        ["Art Events", "Charity Events", "Fashion Events", "Festival", "Social Events", "Sports Events", "Online", "Hybrid"]
    )

    # Event-specific details
    event_capacity = st.number_input("Event Capacity", min_value=1, step=1)
    event_ticket_price = st.number_input("Ticket Price (in ZAR)", min_value=0.0, format="%.2f")

    # Venue and location for physical events
    event_venue_title = st.text_input("Venue Title") if event_category != "Online" else "N/A"
    event_google_maps_location = st.text_input("Google Maps Location") if event_category != "Online" else "N/A"
    event_city = st.text_input("City") if event_category != "Online" else "N/A"
    event_province = st.text_input("Province") if event_category != "Online" else "N/A"

    event_start_date = st.date_input("Event Start Date")
    event_start_time = st.time_input("Event Start Time")

    event_url = st.text_input("Event URL") if event_category in ["Online", "Hybrid"] else "N/A"

    if st.button("Next"):
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
        st.session_state.page = "upload_picture"
        st.experimental_rerun()


def upload_picture_page():
    st.markdown("<h3 style='text-align: center;'>Upload Event Picture</h3>", unsafe_allow_html=True)
    st.write("Upload a picture for your event.")

    event_picture = st.file_uploader("Upload Event Picture", type=["jpg", "jpeg", "png"])

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back"):
            st.session_state.page = "create"
            st.experimental_rerun()

    with col2:
        if event_picture and st.button("Next"):
            st.session_state["event_picture"] = event_picture
            st.session_state.page = "summary"
            st.experimental_rerun()


def summary_page():
    st.markdown("<h3 style='text-align: center;'>Event Summary & Banking Details</h3>", unsafe_allow_html=True)

    st.write("### Event Preview")
    st.write(f"**Title:** {st.session_state.get('event_title', 'N/A')}")
    st.write(f"**Description:** {st.session_state.get('event_description', 'N/A')}")
    st.write(f"**Category:** {st.session_state.get('event_category', 'N/A')}")
    st.write(f"**Capacity:** {st.session_state.get('event_capacity', 'N/A')}")
    st.write(f"**Ticket Price:** {st.session_state.get('event_ticket_price', 'N/A')} ZAR")
    st.write(f"**Venue Title:** {st.session_state.get('event_venue_title', 'N/A')}")
    st.write(f"**Google Maps Location:** {st.session_state.get('event_google_maps_location', 'N/A')}")
    st.write(f"**City:** {st.session_state.get('event_city', 'N/A')}")
    st.write(f"**Province:** {st.session_state.get('event_province', 'N/A')}")
    st.write(f"**Start Date:** {st.session_state.get('event_start_date', 'N/A')}")
    st.write(f"**Start Time:** {st.session_state.get('event_start_time', 'N/A')}")
    st.write(f"**Event URL:** {st.session_state.get('event_url', 'N/A')}")

    if "event_picture" in st.session_state:
        st.image(st.session_state["event_picture"], caption="Event Picture", use_column_width=True)

    st.write("### Enter Your Banking Details")
    bank_account_number = st.text_input("Bank Account Number")
    bank_name = st.selectbox(
        "Bank Name",
        ["ABSA", "Capitec Bank", "FNB", "Nedbank", "Standard Bank", "Investec", "TymeBank", "African Bank", "Bidvest Bank", "Discovery Bank"]
    )
    account_holder = st.text_input("Account Holder Name")
    branch_code = st.text_input("Branch Code")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back"):
            st.session_state.page = "upload_picture"
            st.experimental_rerun()

    with col2:
        if bank_account_number and account_holder and branch_code and st.button("Submit"):
            st.success("🎉 Event successfully created and banking details submitted! 🎉")
            # Clear session state to start fresh
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()


# Navigation between pages
if st.session_state.page == "create":
    create_page()
elif st.session_state.page == "upload_picture":
    upload_picture_page()
elif st.session_state.page == "summary":
    summary_page()
