import streamlit as st
import psycopg2
from establish_connection import connect_to_database

def insert_event_data(event_data):
    """Inserts event and organizer details into the database."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()

            # Insert location
            location_query = '''
            INSERT INTO "Location" (province, city, venue_title, google_maps)
            VALUES (%s, %s, %s, %s)
            RETURNING location_id
            '''
            cursor.execute(location_query, (
                event_data['province'], event_data['city'], 
                event_data['venue_title'], event_data['google_maps_location']
            ))
            location_id = cursor.fetchone()[0]

            # Insert category
            category_query = '''
            INSERT INTO "Category" (category)
            VALUES (%s)

            RETURNING category_id
            '''
            cursor.execute(category_query, (event_data['event_category'],))
            category_result = cursor.fetchone()
            if category_result:
                category_id = category_result[0]
            else:
                cursor.execute('SELECT category_id FROM "Category" WHERE category = %s', (event_data['event_category'],))
                category_id = cursor.fetchone()[0]

            # Insert organizer (banking details included)
            organizer_query = '''
            INSERT INTO "Organizer" (name, email, phone_number, bank_name, bank_account_number, account_holder_name, bank_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING organizer_id
            '''
            cursor.execute(organizer_query, (
                event_data['organizer_name'], event_data['organizer_email'], event_data['phone_number'],
                event_data['bank_name'], event_data['bank_account_number'], event_data['account_holder_name'],
                event_data['bank_code']
            ))
            organizer_id = cursor.fetchone()[0]

            # Insert event (including the image path)
            event_query = '''
            INSERT INTO "Events" (capacity, start_date, start_time, description, event_title, location_id, category_id, price, event_url, organizer_id, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(event_query, (
                event_data['capacity'], event_data['start_date'], event_data['start_time'], 
                event_data['description'], event_data['title'], location_id, category_id, 
                event_data['ticket_price'], event_data['event_url'], organizer_id, event_data.get('image', None)
            ))

            conn.commit()
            st.success("Event created successfully!")
            # Reset session state after submission
            st.session_state.step = 1
            st.session_state.event_data = {}
        except Exception as e:
            st.error(f"Error inserting event: {e}")
        finally:
            cursor.close()
            conn.close()

def event_form():
    """Streamlit multi-step event creation form."""
    st.title("Create an Event")
    
    # Initialize session state variables
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "event_data" not in st.session_state:
        st.session_state.event_data = {}

    # Step 1: Event Details
    if st.session_state.step == 1:
        st.write("### Event Details")
        event_category = st.selectbox("Category", ["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival", "Fashion Event"], 
                                      index=["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival", "Fashion Event"].index(st.session_state.event_data.get('event_category', "Online Event")))
        title = st.text_input("Event Title", st.session_state.event_data.get('title', ""))
        description = st.text_area("Event Description", st.session_state.event_data.get('description', ""))
        capacity = st.number_input("Capacity", min_value=1, step=1, value=st.session_state.event_data.get('capacity', 1))
        ticket_price = st.number_input("Ticket Price (ZAR)", min_value=0.0, step=0.01, value=st.session_state.event_data.get('ticket_price', 0.0))
        
        if event_category != "Online Event":
            venue_title = st.text_input("Venue Title", st.session_state.event_data.get('venue_title', ""))
            google_maps_location = st.text_input("Google Maps Location", st.session_state.event_data.get('google_maps_location', ""))
            city = st.text_input("City", st.session_state.event_data.get('city', ""))
            province = st.text_input("Province", st.session_state.event_data.get('province', ""))
        else:
            venue_title, google_maps_location, city, province = None, None, None, None
        
        event_url = st.text_input("Event URL", st.session_state.event_data.get('event_url', ""))
        start_date = st.date_input("Start Date", st.session_state.event_data.get('start_date', None))
        start_time = st.time_input("Start Time", st.session_state.event_data.get('start_time', None))
        
        # Add Image Upload
        image = st.file_uploader("Upload Event Image", type=["jpg", "png", "jpeg"])
        if image is not None:
            st.session_state.event_data['image'] = image.name  # Store the image file name or path
        
        if st.button("Next", key="next_1"):
            st.session_state.event_data.update({
                'event_category': event_category,
                'title': title,
                'description': description,
                'capacity': capacity,
                'ticket_price': ticket_price,
                'venue_title': venue_title,
                'google_maps_location': google_maps_location,
                'city': city,
                'province': province,
                'start_date': start_date,
                'start_time': start_time,
                'event_url': event_url
            })
            st.session_state.step = 2

    # Step 2: Organizer Details
    elif st.session_state.step == 2:
        st.write("### Event Organizer Information")
        name = st.text_input("Name", st.session_state.event_data.get('organizer_name', ""))
        email = st.text_input("Email", st.session_state.event_data.get('organizer_email', ""))
        phone_number = st.text_input("Phone Number", st.session_state.event_data.get('phone_number', ""))
        bank_name = st.text_input("Bank Name", st.session_state.event_data.get('bank_name', ""))
        bank_account_number = st.text_input("Bank Account Number", st.session_state.event_data.get('bank_account_number', ""))
        account_holder_name = st.text_input("Account Holder Name", st.session_state.event_data.get('account_holder_name', ""))
        bank_code = st.text_input("Branch Code", st.session_state.event_data.get('bank_code', ""))
        
        if st.button("Next", key="next_2"):
            st.session_state.event_data.update({
                'organizer_name': name,
                'organizer_email': email,
                'phone_number': phone_number,
                'bank_name': bank_name,
                'bank_account_number': bank_account_number,
                'account_holder_name': account_holder_name,
                'bank_code': bank_code
            })
            st.session_state.step = 3

    # Step 3: Event Preview & Submission
    elif st.session_state.step == 3:
        st.write("### Event Preview")

        # Create a nice preview layout
        preview_html = f"""
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
            <h2 style="text-align: center; color: #4CAF50;">{st.session_state.event_data['title']}</h2>
            <div style="text-align: center;">
                <img src="{st.session_state.event_data['image']}" alt="Event Image" style="width: 100%; max-width: 400px; border-radius: 10px;">
            </div>
            <p><strong>Description:</strong> {st.session_state.event_data['description']}</p>
            <p><strong>Category:</strong> {st.session_state.event_data['event_category']}</p>
            <p><strong>Venue:</strong> {st.session_state.event_data.get('venue_title', 'N/A')}</p>
            <p><strong>Location:</strong> {st.session_state.event_data.get('city', '')}, {st.session_state.event_data.get('province', '')}</p>
            <p><strong>Start Date:</strong> {st.session_state.event_data['start_date']}</p>
            <p><strong>Start Time:</strong> {st.session_state.event_data['start_time']}</p>
            <p><strong>Capacity:</strong> {st.session_state.event_data['capacity']}</p>
            <p><strong>Ticket Price:</strong> ZAR {st.session_state.event_data['ticket_price']}</p>
            <p><strong>Event URL:</strong> <a href="{st.session_state.event_data['event_url']}" target="_blank">Click here</a></p>
        </div>
        """

        st.markdown(preview_html, unsafe_allow_html=True)

        if st.button("Confirm and Create Event"):
            insert_event_data(st.session_state.event_data)
        elif st.button("Go Back to Edit Organizer Info"):
            st.session_state.step = 2
        elif st.button("Go Back to Edit Event Details"):
            st.session_state.step = 1

if __name__ == "__main__":
    event_form()
