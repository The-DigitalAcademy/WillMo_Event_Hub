import streamlit as st
from datetime import datetime


#image_path = "/Users/tshmacm1172/Downloads/WillMo.jpg"
#st.image(image_path, width=290)
#st.set_page_config(page_title="Willcome to WillMo Events",  layout="wide")
pages = [
    st.Page("app_pages/admin.py", title="Admin", icon="👋"),
   st.Page("app_pages/profile.py", title="Profile", icon="👋"),
]

# Adding pages to the sidebar navigation using st.navigation
pg = st.navigation(pages, position="sidebar", expanded=True)
# Running the app
pg.run()
st.title("WillMo Events Hub")


# Search for an event by title and location
st.subheader("Search for an Event")


# List of major South African cities for location filter
south_african_cities = [
    "All Locations",
    "Cape Town",
    "Johannesburg",
    "Durban",
    "Pretoria",
    "Port Elizabeth",
    "Bloemfontein",
    "East London",
    "Polokwane",
    "Nelspruit",
    "Kimberley",
    "Pietermaritzburg",
    "Vanderbijlpark",
    "George",
    "Rustenburg",
    "Mbombela",
    "Tshwane",
]

# Text input for event title
event_title_search = st.text_input("Search by event title", "")
# Select box for location filter (you can add more locations as needed)

location_search = st.selectbox("Filter by location", south_african_cities)

#  Empty events section with a placeholder for now
st.subheader("Upcoming Events")


