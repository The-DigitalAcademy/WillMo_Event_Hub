import streamlit as st
import psycopg2

# Database connection settings
DB_HOST = "localhost"
DB_NAME = "willmo"
DB_USER = "postgres"
DB_PASSWORD = "Will"
DB_PORT = "5432"  # Default PostgreSQL port

def connect_to_db():
    """Connect to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

def insert_event_data(event_data):
    """Insert event data into multiple database tables."""
    conn = connect_to_db()
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
            st.success("🎉 Event successfully created and stored in the database!")
        
        except Exception as e:
            st.error(f"Error inserting event: {e}")
        
        finally:
            cursor.close()
            conn.close()

def event_form():
    """Render the event creation form in Streamlit."""
    st.title("Create an Event")

    
    event_category = st.selectbox("Event Category", ["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival"])

    
    title = st.text_input("Event Title")
    description = st.text_area("Event Description")
    capacity = st.number_input("Capacity", min_value=1, step=1)
    ticket_price = st.number_input("Ticket Price (ZAR)", min_value=0.0, step=0.01)

    #"
    venue_disabled = event_category == "Online Event"
    venue_title = st.text_input("Venue Title", disabled=venue_disabled)
    google_maps_location = st.text_input("Google Maps Location", disabled=venue_disabled)
    if google_maps_location:
       google_maps_url = f"https://www.google.com/maps/search/?q={google_maps_location}"
       st.markdown(f"[Click to view location on Google Maps]({google_maps_url})", unsafe_allow_html=True)

    city = st.text_input("City", disabled=venue_disabled)
    province = st.text_input("Province", disabled=venue_disabled)
    event_url = st.text_input("Event URL")

    start_date = st.date_input("Start Date")
    start_time = st.time_input("Start Time")
     
    
    if st.button("Create Event"):
        event_data = {
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
        insert_event_data(event_data)

if __name__ == "__main__":
    event_form()
