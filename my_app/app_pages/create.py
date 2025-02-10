import streamlit as st


def create():
    st.markdown("<h3 style='text-align: center;'>Create Event</h3>", unsafe_allow_html=True)
    st.write("Here you can create new events.")
    
    # Form to create an event
    event_title = st.text_input("Event Title")
    event_description = st.text_area("Event Description")
    
    # Dropdown for event categories
    event_category = st.selectbox(
        "Event Category",
        ["Art Events", "Charity Events", "Fashion Events", "Festival", "Social Events", "Sports Events", "Online", "Hybrid"]
    )
    
    # Check if the event is Online or Hybrid
    is_online = event_category == "Online"
    is_hybrid = event_category == "Hybrid"

    # Enable or disable fields based on event category
    event_capacity = st.number_input("Event Capacity", min_value=1, step=1) if not is_online else st.number_input("Event Capacity", min_value=1, step=1)
    event_ticket_price = st.number_input("Ticket Price (in ZAR)", min_value=0.0, format="%.2f") if not is_online else st.number_input("Ticket Price (in ZAR)", min_value=0.0, format="%.2f")
    
    # Venue and location fields (Disabled for Online events only)
    event_venue_title = st.text_input("Venue Title") if not is_online else st.text_input("Venue Title", disabled=True)
    event_google_maps_location = st.text_input("Google Maps Location") if not is_online else st.text_input("Google Maps Location", disabled=True)
    event_city = st.text_input("City") if not is_online else st.text_input("City", disabled=True)
    event_province = st.text_input("Province") if not is_online else st.text_input("Province", disabled=True)
    
    # Event start date and time
    event_start_date = st.date_input("Event Start Date") 
    event_start_time = st.time_input("Event Start Time")

    # Event URL (enabled for Online and Hybrid events only)
    event_url = st.text_input("Event URL") if is_online or is_hybrid else st.text_input("Event URL", disabled=True)

    # Event description for Online or Hybrid events
    if is_online:
        st.write(f"This event will be held online.")
    elif is_hybrid:
        st.write(f"This event will be a Hybrid event (both online and in-person).")
    
    # Save the event data in session state when the 'Next' button is clicked
    if st.button("Next"):
        # Save event data in session state
        st.session_state.event_title = event_title
        st.session_state.event_description = event_description
        st.session_state.event_category = event_category
        st.session_state.event_capacity = event_capacity
        st.session_state.event_ticket_price = event_ticket_price
        st.session_state.event_venue_title = event_venue_title if not is_online else 'N/A'
        st.session_state.event_google_maps_location = event_google_maps_location if not is_online else 'N/A'
        st.session_state.event_city = event_city if not is_online else 'N/A'
        st.session_state.event_province = event_province if not is_online else 'N/A'
        st.session_state.event_start_date = event_start_date
        st.session_state.event_start_time = event_start_time
        st.session_state.event_url = event_url if is_online or is_hybrid else 'N/A'
        
        # Move to the upload picture page
        st.session_state.show_create = False  # Hide create event page
        st.session_state.show_upload_picture = True  # Show upload picture page

def display_upload_picture_page():
    st.markdown("<h3 style='text-align: center;'>Upload Event Picture</h3>", unsafe_allow_html=True)
    st.write("Upload a picture for your event.")
    
    event_picture = st.file_uploader("Upload Event Picture", type=["jpg", "jpeg", "png"])

    if st.button("Back"):
        st.session_state.show_upload_picture = False
        st.session_state.show_create = True  # Show the create event page again
        return

    if event_picture and st.button("Next"):
        # Save the uploaded picture in session state
        st.session_state.event_picture = event_picture

        # Show the summary and banking details page
        st.session_state.show_upload_picture = False  # Hide the upload picture page
        st.session_state.show_summary = True  # Show summary and banking details page

def display_summary_and_banking_page():
    st.markdown("<h3 style='text-align: center;'>Event Summary & Banking Details</h3>", unsafe_allow_html=True)

    # Display event preview
    st.write("### Event Preview")
    st.write(f"**Title:** {st.session_state.event_title}")
    st.write(f"**Description:** {st.session_state.event_description}")
    st.write(f"**Category:** {st.session_state.event_category}")
    st.write(f"**Capacity:** {st.session_state.event_capacity}")
    st.write(f"**Ticket Price:** {st.session_state.event_ticket_price} ZAR")
    st.write(f"**Venue Title:** {st.session_state.event_venue_title}")
    st.write(f"**Google Maps Location:** {st.session_state.event_google_maps_location}")
    st.write(f"**City:** {st.session_state.event_city}")
    st.write(f"**Province:** {st.session_state.event_province}")
    st.write(f"**Start Date:** {st.session_state.event_start_date}")
    st.write(f"**Start Time:** {st.session_state.event_start_time}")
    st.write(f"**Event URL:** {st.session_state.event_url}")
    
    if 'event_picture' in st.session_state:
        st.image(st.session_state.event_picture, caption="Event Picture", use_column_width=True)

    # Banking details input
    st.write("### Enter Your Banking Details")
    bank_account_number = st.text_input("Bank Account Number")
    bank_name = st.selectbox("Bank Name", ["ABSA", "Capitec Bank", "FNB (First National Bank)", "Nedbank", "Standard Bank", "Investec", "TymeBank", "African Bank", "Bidvest Bank", "Discovery Bank"])
    account_holder = st.text_input("Account Holder Name")
    branch_code = st.text_input("Branch Code")

    # Submit Button to finalize the event
    if st.button("Submit Event"):
        if bank_account_number and account_holder and branch_code:
            st.success("🎉 Event successfully created and banking details submitted! 🎉")
            st.write(f"**Bank Account Number:** {bank_account_number}")
            st.write(f"**Bank Name:** {bank_name}")
            st.write(f"**Account Holder Name:** {account_holder}")
            st.write(f"**Branch Code:** {branch_code}")
            
            # Reset session state
            st.session_state.show_summary = False
            st.session_state.show_create = False
            st.session_state.show_main = True
        else:
            st.error("Please fill in all banking details before submitting.")

# Main page logic
def list_events_page():
    st.markdown("<h1 style='text-align: center;'>Event Management Hub</h1>", unsafe_allow_html=True)
    st.subheader("Upcoming Events")

    # Show main event list content if show_main is True
    if st.session_state.get("show_main", True):
        selection = st.selectbox("What would you like to do?", ["", "Book an Event", "Create an Event"])

        if selection == "Book an Event":
            st.session_state.show_booking = True
            st.session_state.show_main = False
            st.rerun()  # Refresh content to show booking section

        elif selection == "Create an Event":
            st.session_state.show_create = True
            st.session_state.show_main = False
            st.rerun()

    # Conditional rendering for different pages
    if st.session_state.get("show_create", False):
        create()
    elif st.session_state.get("show_upload_picture", False):
        display_upload_picture_page()
    elif st.session_state.get("show_summary", False):
        display_summary_and_banking_page()

# Run the list events page logic
list_events_page()
