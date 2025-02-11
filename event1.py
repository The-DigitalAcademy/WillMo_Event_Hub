import psycopg2 as ps
import pandas as pd
import streamlit as st
from establish_connection import connect_to_database


# --- Database Connection and Data Fetching Functions ---

def fetch_events(connection, query, params):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params) #queries and parameters you wanna pass
            data = cursor.fetchall()  #get everything
            columns = [desc[0] for desc in cursor.description] if cursor.description else [] #gets all column names
            if data:
                return pd.DataFrame(data, columns=columns)
            else:
                return pd.DataFrame(columns=columns) #turns everything into a table
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# ---Display the List of Events (Booking Page) ---

def display_booking_page():

    # Search bar and filters
    with st.container():
        st.subheader("Search and Filter Events")
        search_query = st.text_input("Search events by name:", placeholder="Enter event name")
        col1, col2, col3 = st.columns(3) #define 3 columns
        with col1:
            selected_date = st.date_input("Select Date", value=None)
        with col2:
            category = st.selectbox(
                "Category",
                ["All", "Charity Event", "Fashion Event", "Festival", "Art Event", 
                 "Social Event", "Sports", "Online Event", "Hybrid Event"]
            )
        with col3:
            province = st.selectbox(
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
    if connection: #this will only happen if there is a successful connection
        
        #get event data from database
        query = """ 
            SELECT e.event_id, e.event_title, e.image, e.start_date, e.start_time, e.price, e.quantity,
                   c.category, l.city, l.province 
            FROM "Events" e
            INNER JOIN "Category" c ON e.category_id = c.category_id
            INNER JOIN "Location" l ON e.location_id = l.location_id
            WHERE 1=1
        """
        params = [] #empty list to store search and

        # Append filters
        if search_query:
            query += " AND e.event_title ILIKE %s"
            params.append(f"%{search_query}%")
        if selected_date:
            query += " AND e.start_date = %s"
            params.append(selected_date)
        if category != "All":
            query += " AND LOWER(c.category) = LOWER(%s)"
            params.append(category)
        if province != "All":
            query += " AND l.province = %s"
            params.append(province)

        events = fetch_events(connection, query, params)

        if not events.empty:
            st.write(f"Found {len(events)} events:")
            # Display 3 cards per row)
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

