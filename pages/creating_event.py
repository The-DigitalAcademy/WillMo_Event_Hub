import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import os
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page  # Importing the switch_page method

def get_customer_details(email):
    """Fetch customer details based on email."""
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT name, surname, contact FROM "Customers" WHERE email = %s', (email,))
            return cursor.fetchone()
    st.error("Database connection failed.")
    return None

def insert_location(province, city, latitude, longitude):
    """Insert location into database and return location_id."""
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            google_maps = f"{latitude},{longitude}"  
            cursor.execute("""
                INSERT INTO "Location" (province, city, google_maps)
                VALUES (%s, %s, %s)
                RETURNING location_id
            """, (province, city, google_maps))
            location_id = cursor.fetchone()[0]  
            conn.commit()
            return location_id
    st.error("Location insertion failed.")
    return None

def insert_category(category):
    """Insert category only if it doesn't exist, then return category_id."""
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT category_id FROM "Category" WHERE category = %s', (category,))
            result = cursor.fetchone()
            if result:
                return result[0]
            cursor.execute('INSERT INTO "Category" (category) VALUES (%s) RETURNING category_id', (category,))
            category_id = cursor.fetchone()[0]
            conn.commit()
            return category_id
    st.error("Category insertion failed.")
    return None

def create_event(event_title, description, start_date, start_time, capacity, quantity, price, event_url, image, province, city, category, organizer_email, bank_name, account_number, account_holder, bank_code, latitude, longitude):
    """Create a new event and insert it into the database."""
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            location_id = insert_location(province, city, latitude, longitude) if category != "Online Event" else None
            category_id = insert_category(category)

            cursor.execute("""
                INSERT INTO "Organizer" (email, bank_name, bank_account_number, account_holder_name, bank_code)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING organizer_id
            """, (organizer_email, bank_name, account_number, account_holder, bank_code))
            organizer_result = cursor.fetchone()
            organizer_id = organizer_result[0] if organizer_result else None

            if not organizer_id:
                cursor.execute('SELECT organizer_id FROM "Organizer" WHERE email = %s', (organizer_email,))
                organizer_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO "Events" (event_title, description, start_date, start_time, capacity, quantity, price, event_url, image, location_id, category_id, organizer_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (event_title, description, start_date, start_time, capacity, quantity, price, event_url, image, location_id, category_id, organizer_id))

            conn.commit()
            st.success("Event created successfully!")

            # Show 'Track Event' button after event is created
            if st.button("Track Event"):
                switch_page("Profile")  # This switches to the Profile.py page

    else:
        st.error("Unable to connect to the database.")

def display_create_event_page():
    """Render the event creation page."""
    st.title("Create New Event")
    email = st.session_state.get("email", "")

    customer_details = get_customer_details(email)
    if not customer_details:
        st.error("Customer details not found. Please register.")
        st.stop()

    name, surname, contact = customer_details

    st.subheader("Organizer Details")
    st.write(f"**Organizer Name**: {name} {surname}")
    st.write(f"**Organizer Contact**: {contact}")
    st.write(f"**Organizer Email**: {email}")

    st.subheader("Event Details")
    event_categories = ["Online Event", "Art Event", "Social Event", "Sports", "Hybrid Event", "Festival", "Fashion Event"]
    category = st.selectbox("Select Event Category", event_categories)
    
    event_title = st.text_input("Event Title")
    description = st.text_area("Event Description")
    start_date = st.date_input("Event Date")
    start_time = st.time_input("Event Time")
    capacity = st.number_input("Event Capacity", min_value=1)
    quantity = st.number_input("Ticket Quantity", min_value=1)
    price = st.number_input("Ticket Price ($)", min_value=0.0, format="%.2f")
    event_url = st.text_input("Event URL", disabled=(category not in ["Online Event", "Hybrid Event"]))
    image_file = st.file_uploader("Upload Event Image", type=["jpg", "jpeg", "png"])

    if category != "Online Event":
        st.subheader("Event Location")
        province = st.text_input("Province")
        city = st.text_input("City")

        latitude, longitude = None, None  
        map_location = folium.Map(location=[-26.2041, 28.0473], zoom_start=10)

        # Enable only marker drawing
        draw = Draw(export=True, draw_options={"marker": True, "polyline": False, "polygon": False, "rectangle": False, "circle": False})
        draw.add_to(map_location)

        map_interaction = st_folium(map_location, width=725)

        if map_interaction and map_interaction.get("last_active_drawing"):
            drawn_data = map_interaction["last_active_drawing"]
            if drawn_data["geometry"]["type"] == "Point":
                longitude, latitude = drawn_data["geometry"]["coordinates"]
                st.write(f"Coordinates: Latitude: {latitude}, Longitude: {longitude}")
    else:
        province, city, latitude, longitude = None, None, None, None  # Disable location input

    st.subheader("Banking Details")
    bank_name = st.text_input("Bank Name")
    account_number = st.text_input("Bank Account Number")
    account_holder = st.text_input("Account Holder Name")
    bank_code = st.text_input("Bank Code")

    image = None
    if image_file:
        image_path = f"event_images/{image_file.name}"
        os.makedirs("event_images", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())
        image = f"/{image_path}"

    if st.button("Create Event"):
        if image is None:
            st.error("Please upload an event image.")
        else:
            create_event(event_title, description, start_date, start_time, capacity, quantity, price, event_url, image, province, city, category, email, bank_name, account_number, account_holder, bank_code, latitude, longitude)

display_create_event_page()
