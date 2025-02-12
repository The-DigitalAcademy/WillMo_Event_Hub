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
            cursor.execute(location_query, (event_data['province'], event_data['city'], event_data['venue_title'], event_data['google_maps_location']))
            location_id = cursor.fetchone()[0]

            category_query = '''
            INSERT INTO "Category" (category)
            VALUES (%s)
            ON CONFLICT (category) DO NOTHING
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
            
        except Exception as e:
            st.error(f"Error inserting event: {e}")
        
        finally:
            cursor.close()
            conn.close()

def event_form():
    
    # Add custom CSS to style the page
    st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
            margin-top: 10px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stSelectbox, .stTextInput, .stTextArea, .stNumberInput, .stDateInput, .stTimeInput {
            width: 100%;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }
        .form-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .header {
            text-align: center;
            color: #333;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Create an Event")

    # Initialize session state
    if "show_event_form" not in st.session_state:
        st.session_state.show_event_form = True
    if "event_data" not in st.session_state:
        st.session_state.event_data = {}

    if st.session_state.show_event_form:
        st.write("### Event Details")
        
        event_category = st.selectbox("Category", ["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival", "Fashion Event"])
        title = st.text_input("Event Title")
        description = st.text_area("Event Description")
        capacity = st.number_input("Capacity", min_value=1, step=1)
        ticket_price = st.number_input("Ticket Price (ZAR)", min_value=0.0, step=0.01)
        venue_title = st.text_input("Venue Title", disabled=event_category == "Online Event")
        google_maps_location = st.text_input("Google Maps Location", disabled=event_category == "Online Event")
        city = st.text_input("City", disabled=event_category == "Online Event")
        province = st.text_input("Province", disabled=event_category == "Online Event")
        event_url = st.text_input("Event URL", disabled=event_category in ["Art Event", "Social Event", "Sports", "Festival", "Fashion Event"])
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time")

        if st.button("Next"):
            # Save event data in session state
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
            st.session_state.show_event_form = False

    elif not st.session_state.show_event_form:
        st.write("### Event Organizer Information")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        bank_name = st.text_input("Bank Name")
        bank_account_number = st.text_input("Bank Account Number")
        account_holder_name = st.text_input("Account Holder Name") 
        bank_code = st.text_input("Branch Code")

        if st.button("Preview"):
            # Save organizer information
            st.session_state.event_data.update({
                'organizer_name': name,
                'email': email,
                'phone_number': phone_number,
                'bank_name': bank_name,
                'bank_account_number': bank_account_number,
                'account_holder_name': account_holder_name,
                'bank_code': bank_code
            })

            st.session_state.show_event_form = False
            st.session_state.show_preview = True

    if 'show_preview' in st.session_state and st.session_state.show_preview:
        st.write("### Preview Event Details")
        event_data = st.session_state.event_data
        
        st.write(f"**Event Title**: {event_data['title']}")
        st.write(f"**Category**: {event_data['event_category']}")
        st.write(f"**Description**: {event_data['description']}")
        st.write(f"**Capacity**: {event_data['capacity']}")
        st.write(f"**Ticket Price (ZAR)**: {event_data['ticket_price']}")
        st.write(f"**Start Date**: {event_data['start_date']}")
        st.write(f"**Start Time**: {event_data['start_time']}")
        
        st.write("### Organizer Details")
        st.write(f"**Name**: {event_data['organizer_name']}")
        st.write(f"**Email**: {event_data['email']}")
        st.write(f"**Phone Number**: {event_data['phone_number']}")
        st.write(f"**Bank Name**: {event_data['bank_name']}")
        st.write(f"**Bank Account Number**: {event_data['bank_account_number']}")
        st.write(f"**Account Holder Name**: {event_data['account_holder_name']}")
        st.write(f"**Bank Code**: {event_data['bank_code']}")
        
        if st.button("Confirm"):
            insert_event_data(event_data)
            st.session_state.show_preview = False
            st.session_state.show_congratulations = True

    if 'show_congratulations' in st.session_state and st.session_state.show_congratulations:
        st.write("### Congratulations!")
        st.write("Your event has been successfully created.")
        st.write("You can now track the performance of your event by clicking the link below:")
        st.markdown("[Track your event](#)")

        # Reset for a new event
        st.session_state.show_event_form = True
        st.session_state.show_congratulations = False
