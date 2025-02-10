import streamlit as st

def home():

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

if __name__ == "__page__":
    home()
