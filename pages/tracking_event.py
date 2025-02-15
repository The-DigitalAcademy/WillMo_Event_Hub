import streamlit as st
import psycopg2
import pandas as pd

# Function to connect to the database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='willmo',  
            user='postgres',     
            password='Will'      
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to track ticket sales
def track_sales():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("You must be signed in to proceed.")
        return

    email = st.session_state.get("email", None)
    if not email:
        st.error("No email found. Please log in.")
        return

    conn = connect_to_database()
    if not conn:
        return
    
    cursor = conn.cursor()

    try:
        # Fetch organiser ID from email
        cursor.execute('SELECT organizer_id FROM "Organizer" WHERE email = %s', (email,))
        organiser_id_result = cursor.fetchone()
        if not organiser_id_result:
            st.error("You are not registered as an organiser.")
            return
        organiser_id = organiser_id_result[0]

        # Get ticket sales data for organiser's events
        query = '''
            SELECT e.event_title, SUM(bem.event_id) AS tickets_sold
            FROM "Events" e
            JOIN "BookingEventMap" bem ON e.event_id = bem.event_id
            WHERE e.organizer_id = %s
            GROUP BY e.event_title
            ORDER BY tickets_sold DESC
        '''
        cursor.execute(query, (organiser_id,))
        sales_data = cursor.fetchall()

        # Display results
        if sales_data:
            df = pd.DataFrame(sales_data, columns=["Event", "Tickets Sold"])
            st.subheader("Ticket Sales Overview")
            st.dataframe(df)
        else:
            st.info("No ticket sales yet.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()

# Display organiser dashboard
def display_organiser_dashboard():
    st.title("Organiser Dashboard")

    if st.button("Track Ticket Sales"):
        track_sales()

# Run the organiser dashboard function
display_organiser_dashboard()
