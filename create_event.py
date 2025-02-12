import streamlit as st
import psycopg2
from establish_connection import connect_to_database

def insert_event_data(event_data):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()

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

            event_query = '''
            INSERT INTO "Events" (capacity, start_date, start_time, description, event_title, location_id, category_id, price, event_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(event_query, (
                event_data['capacity'], event_data['start_date'], event_data['start_time'], 
                event_data['description'], event_data['title'], location_id, category_id, 
                event_data['ticket_price'], event_data['event_url']
            ))

            conn.commit()
            st.success("Event created successfully!")
        except Exception as e:
            st.error(f"Error inserting event: {e}")
        finally:
            cursor.close()
            conn.close()

def event_form():
    st.title("Create an Event")
    
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "event_data" not in st.session_state:
        st.session_state.event_data = {}

    if st.session_state.step == 1:
        st.write("### Event Details")
        event_category = st.selectbox("Category", ["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival", "Fashion Event"])
        title = st.text_input("Event Title")
        description = st.text_area("Event Description")
        capacity = st.number_input("Capacity", min_value=1, step=1)
        ticket_price = st.number_input("Ticket Price (ZAR)", min_value=0.0, step=0.01)
        
        if event_category != "Online Event":
            venue_title = st.text_input("Venue Title")
            google_maps_location = st.text_input("Google Maps Location")
            city = st.text_input("City")
            province = st.text_input("Province")
        else:
            venue_title, google_maps_location, city, province = None, None, None, None
        
        event_url = st.text_input("Event URL")
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time")
        
        if st.button("Next"):
            st.session_state.event_data = {
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
            }
            st.session_state.step = 2

    elif st.session_state.step == 2:
        st.write("### Event Organizer Information")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        bank_name = st.text_input("Bank Name")
        bank_account_number = st.text_input("Bank Account Number")
        account_holder_name = st.text_input("Account Holder Name")
        bank_code = st.text_input("Branch Code")
        
        if st.button("Next"):
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

    elif st.session_state.step == 3:
        st.write("### Event Preview")
        for key, value in st.session_state.event_data.items():
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        if st.button("Confirm and Create Event"):
            insert_event_data(st.session_state.event_data)
            st.session_state.step = 1  # Reset after submission
        elif st.button("Go Back to Edit Event"):
            st.session_state.step = 1

if __name__ == "__main__":
    event_form()