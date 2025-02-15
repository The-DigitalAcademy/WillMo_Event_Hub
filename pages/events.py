import streamlit as st
import pandas as pd
import os
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page

# Define the local image directory (update this path accordingly)
IMAGE_FOLDER = "/event_images"

def fetch_events(connection, query, params):
    """Fetch events from the database based on query and parameters."""
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        if not result:
            return pd.DataFrame()
        columns = ["event_id", "event_title", "image", "start_date", "start_time", "price", "quantity", "category", "city", "province"]
        return pd.DataFrame(result, columns=columns)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# CSS for styling the event cards
st.markdown(
    """
    <style>
    .card-title { font-size: 16px; font-weight: bold; margin: 10px 0; }
    .card-details { font-size: 14px; color: #666; }
    .card-price { font-size: 14px; font-weight: bold; margin: 10px 0; color: #444; }
    </style>
    """,
    unsafe_allow_html=True
)

def display_booking_page():
    """Displays the event booking page with search and filter options."""
    st.subheader("Search and Filter Events")

    # User input for filtering events
    search_query = st.text_input("Search events by name:", placeholder="Enter event name")
    selected_date = st.date_input("Select Date", value=None)
    category = st.multiselect("Category", ["All", "Charity Event", "Fashion Event", "Festival", "Art Event", "Social Event", "Sports", "Online Event", "Hybrid Event"])
    province = st.multiselect("Province", ["All", "Gauteng", "KwaZulu-Natal", "Eastern Cape", "Free State", "Western Cape", "Northern Cape", "North West", "Mpumalanga", "Limpopo"])

    # Establish database connection
    connection = connect_to_database()
    if not connection:
        st.error("Database connection failed.")
        return

    # Build filters for the SQL query
    filters = []
    if search_query:
        filters.append(("e.event_title ILIKE %s", f"%{search_query}%"))
    if selected_date:
        filters.append(("e.start_date = %s", selected_date))
    if category and "All" not in category:
        filters.append(("LOWER(c.category) IN %s", tuple([cat.lower() for cat in category])))
    if province and "All" not in province:
        filters.append(("l.province IN %s", tuple(province)))

    # Construct the SQL query
    query = """
        SELECT e.event_id, e.event_title, e.image, e.start_date, e.start_time, e.price, e.quantity,
               c.category, l.city, l.province
        FROM "Events" e
        INNER JOIN "Category" c ON e.category_id = c.category_id
        INNER JOIN "Location" l ON e.location_id = l.location_id
    """
    params = []
    if filters:
        filter_clauses, params = zip(*filters)
        query += " WHERE " + " AND ".join(f"({clause})" for clause in filter_clauses)

    # Fetch events from database
    events = fetch_events(connection, query, list(params))

    if events.empty:
        st.info("No events match your search criteria. Showing related events instead.")
        query += " ORDER BY e.start_date ASC LIMIT 10"
        events = fetch_events(connection, query, list(params))

    # Display events in a responsive grid layout
    for i in range(0, len(events), 3):
        row_events = events.iloc[i:i + 3]
        cols = st.columns(3, gap="large")

        for col, (_, event) in zip(cols, row_events.iterrows()):
            with col:
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)

                    # Determine if the image is a URL or a local file
                    image_path = event["image"]
                    if image_path and (image_path.startswith("http") or image_path.startswith("https")):
                        st.image(image_path, use_container_width=True)
                    else:
                        full_image_path = os.path.join(IMAGE_FOLDER, image_path) if image_path else None
                        if full_image_path and os.path.exists(full_image_path):
                            st.image(full_image_path, use_container_width=True)
                        else:
                            st.warning("Image not found")

                    # Display event details
                    st.markdown(f'<div class="card-title">{event["event_title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Date: {event["start_date"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Time: {event["start_time"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Category: {event["category"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Province: {event["province"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">City: {event["city"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-price">Price: R{event["price"]}</div>', unsafe_allow_html=True)

                    # "More Details" button to navigate to event details page
                    if st.button("More Details", key=f"details_{event['event_id']}"):
                        st.session_state["event_id"] = event["event_id"]
                        switch_page("event_details")

                    st.markdown('</div>', unsafe_allow_html=True)

# Run the function to display the booking page
display_booking_page()
