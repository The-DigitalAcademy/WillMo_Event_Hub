import streamlit as st
import psycopg2
from my_app.my_pages.establish_connection import connect_to_database

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
        st.write("### Event Preview")
        st.write(f"**Event Title:** {st.session_state.event_data['title']}")
        st.write(f"**Category:** {st.session_state.event_data['event_category']}")
        st.write(f"**Description:** {st.session_state.event_data['description']}")
        st.write(f"**Capacity:** {st.session_state.event_data['capacity']}")
        st.write(f"**Ticket Price (ZAR):** {st.session_state.event_data['ticket_price']}")
        st.write(f"**Venue Title:** {st.session_state.event_data['venue_title']}")
        st.write(f"**Google Maps Location:** {st.session_state.event_data['google_maps_location']}")
        st.write(f"**City:** {st.session_state.event_data['city']}")
        st.write(f"**Province:** {st.session_state.event_data['province']}")
        st.write(f"**Start Date:** {st.session_state.event_data['start_date']}")
        st.write(f"**Start Time:** {st.session_state.event_data['start_time']}")
        st.write(f"**Event URL:** {st.session_state.event_data['event_url']}")

        if st.button("Confirm and Create Event"):
            # Insert event data into the database
            insert_event_data(st.session_state.event_data)
            
            # Show success message with tracking link
            st.success("Congratulations for creating a new event!")
            st.write("You can now track the performance of your event by clicking the link below:")
            st.markdown("[Track your event](#)")  # Replace '#' with actual tracking link

            st.session_state.show_event_form = True  # Reset for a new event

        elif st.button("Go Back to Edit Event"):
            st.session_state.show_event_form = True  # Go back to event form

if __name__ == "__main__":
    event_form()
