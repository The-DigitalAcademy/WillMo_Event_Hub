import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import psycopg2
from establish_connection import connect_to_database


# Establish Database Connection
conn = connect_to_database()
if conn:
    cursor = conn.cursor()
    user_email = st.session_state.get("email", "")

    if user_email:
        try:
            cursor.execute('SELECT name FROM "Customers" WHERE email = %s', (user_email,))
            user_name = cursor.fetchone()
            if user_name:
                st.session_state["user_name"] = user_name[0]
            else:
                st.session_state["user_name"] = "User"
        except psycopg2.Error as e:
            st.error(f"Error fetching user details: {e}")
else:
    st.error("Unable to connect to the database. Please try again later.")

# Display Logo and Welcome Message
logo_path = "WillMo_Logo.jpg"
st.image(logo_path, width=290)
st.title(f" Welcome, {st.session_state.get('user_name', 'User')}!")
st.subheader("Explore upcoming events and create your own events.")

# Navigation Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("View Events", key="book_event"):
        switch_page("events")  
with col2:
    if st.button("My Profile", key="Profile"):
        switch_page("pages/Profile.py") 
with col3:
    if st.button("Create Event", key="create_event"):
        switch_page("pages/creating_event.py")


st.markdown(
    """
    ### Why Use Event Hub?
    - 🎟️ **Discover & Book Events** – From concerts to conferences, find what excites you!
    - 🛒 **Manage Your Bookings** – View and track your event reservations.
    - 🌍 **Secure & Seamless** – Safe transactions and real-time updates.
    """
)

# Footer
st.markdown("---")
st.write("© 2025 WillMo Event Hub. All rights reserved.")

# Close Database Connection
if conn:
    cursor.close()
    conn.close()
