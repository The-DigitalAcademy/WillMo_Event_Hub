import streamlit as st
from streamlit_extras.switch_page_button import switch_page


# Page Configuration
st.set_page_config(page_title="Event Hub - Dashboard", layout="wide")


# Display Welcome Message
logo_path = "WillMo_Logo.jpg"
logo = st.image(logo_path, width=290)
st.title(f" Welcome, {st.session_state.get('user_name', 'User')}!")
st.subheader("Explore upcoming events and manage your bookings.")

# Navigation Buttons
col1, col2, col3 = st.columns(4)
with col1:
   if st.button("View Events", key="book_event"):
            switch_page("events")  # Redirect to Bookings page
with col2:
    if st.button("⚙️ My Profile",key="Profile"):
        st.switch_page("pages/Profile.py")  # Redirect to profile settings
with col3:
    if st.button("⚙️ create event",key="create_event"):
        st.switch_page("pages/creating_event.py")


# About the Platform
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
