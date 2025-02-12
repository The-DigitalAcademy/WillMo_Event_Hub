import psycopg2 as ps
import pandas as pd
import streamlit as st
from establish_connection import connect_to_database

# --- Database Connection and Data Fetching Functions ---

def fetch_events(connection, query, params):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame(columns=columns)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- Display the List of Events (Booking Page) ---

def display_booking_page():
    # Search bar and filters
    with st.container():
        st.subheader("Search and Filter Events")
        search_query = st.text_input("Search events by name:", placeholder="Enter event name")
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_date = st.date_input("Select Date", value=None)
        with col2:
            category = st.multiselect(
                
                "Category",
                ["All", "Charity Event", "Fashion Event", "Festival", "Art Event", 
                 "Social Event", "Sports", "Online Event", "Hybrid Event"]
            )
        with col3:
            province = st.multiselect(

                "Province",
                ["All", "Gauteng", "KwaZulu-Natal", "Eastern Cape", "Free State", 
                 "Western Cape", "Northern Cape", "North West", "Mpumalanga", "Limpopo"]
            )

    # CSS for card styling
    st.markdown("""
        <style>
        .event-card {
            border: 1px solid #ccc;
            padding: 16px;
            margin: 10px;
            border-radius: 8px;
            height: 550px;
        }
        .event-card img {
            max-height: 200px;
            margin-bottom: 10px;
        }
        .event-card h3 {
            font-size: 1.2em;
            margin-bottom: 8px;
        }
        .event-card p {
            font-size: 1em;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Fetch and display events
    connection = connect_to_database()
    if connection:
        # Build dynamic filters
        filters = []
        if search_query:
            filters.append(("e.event_title ILIKE %s", f"%{search_query}%"))
        if selected_date:
            filters.append(("e.start_date = %s", selected_date))
        if category != "All":
            filters.append(("LOWER(c.category) = LOWER(%s)", category))
        if province != "All":
            filters.append(("l.province = %s", province))

        # Base query
        query = """ 
            SELECT e.event_id, e.event_title, e.image, e.start_date, e.start_time, e.price, e.quantity,
                   c.category, l.city, l.province 
            FROM "Events" e
            INNER JOIN "Category" c ON e.category_id = c.category_id
            INNER JOIN "Location" l ON e.location_id = l.location_id
        """

        # Add filters dynamically
        if filters:
            filter_clauses, params = zip(*filters)
            query += " WHERE " + " OR ".join(f"({clause})" for clause in filter_clauses)
        else:
            params = []

        events = fetch_events(connection, query, list(params))

        if not events.empty:
            st.write(f"Found {len(events)} events:")
            # Display 3 cards per row
            for i in range(0, len(events), 3):
                row_events = events.iloc[i:i + 3]
                cols = st.columns(3)
                for col, (_, event) in zip(cols, row_events.iterrows()):
                    with col:
                        # Wrap the entire card in an anchor tag that passes the event_id.
                        st.markdown(f"""
                            <a href="?event_id={event['event_id']}" style="text-decoration: none; color: inherit;">
                                <div class="event-card">
                                    <img src="{event['image']}" alt="Event Image">
                                    <h3>{event['event_title']}</h3>
                                    <p><strong>Date and Time:</strong> {event['start_date']} at {event['start_time']}</p>
                                    <p><strong>Category:</strong> {event['category']}</p>
                                    <p><strong>Location:</strong> {event['city']}, {event['province']}</p>
                                    <p><strong>Price:</strong> R{event['price']}</p>
                                    <p><strong>Available Tickets:</strong> {event['quantity']}</p>
                                </div>
                            </a>
                        """, unsafe_allow_html=True)
        else:
            if selected_date:
                st.info(f"No events found for the selected date: {selected_date}")
            else:
                st.info("No events match your search criteria.")
    else:
        st.error("Could not connect to the database.")

# --- Page to Display the Details of a Specific Event ---

def display_event_details_page(event_id):
    st.title("Event Details")
    connection = connect_to_database()
    if connection:
        query = """
            SELECT e.event_id, e.event_title, e.image, e.description, e.price, e.quantity, 
                   l.venue_title, l.province, l.city, l.google_maps,
                   c.category, cu.contact, cu.name, cu.surname
            FROM "Events" e
            INNER JOIN "Category" c ON e.category_id = c.category_id
            INNER JOIN "Location" l ON e.location_id = l.location_id
            LEFT JOIN "CustomerMap" cm ON cm.event_id = e.event_id
            LEFT JOIN "Customers" cu ON cu.email = cm.email
            WHERE e.event_id = %s
        """
        params = [event_id]
        event_df = fetch_events(connection, query, params)
        if not event_df.empty:
            event = event_df.iloc[0]
            st.image(event['image'], use_column_width=True)
            st.header(event['event_title'])
            st.subheader("Description")
            st.write(event['description'])
            st.subheader("Location Details")
            st.write(f"**Venue:** {event['venue_title']}")
            st.write(f"**City:** {event['city']}")
            st.write(f"**Province:** {event['province']}")
            st.write(f"**Google Maps:** [View Location]({event['google_maps']})")
            st.subheader("Ticket Information")
            st.write(f"**Price:** R{event['price']}")
            st.write(f"**Available Tickets:** {event['quantity']}")
            
            if pd.notna(event['contact']):
                st.subheader("Contact Information")
                st.write(f"**Name:** {event['name']} {event['surname']}")
                st.write(f"**Contact Number:** {event['contact']}")
            else:
                st.write("No contact information available.")
        else:
            st.error("Event not found.")
    else:
        st.error("Could not connect to the database.")

    # Back link and Book Now button
    st.markdown('<a href="/" style="text-decoration: none;">&larr; Back to Events</a>', unsafe_allow_html=True)
    if st.button("Book Now"):
        st.session_state["page"] = "checkout"
        st.session_state["event_id"] = event_id
