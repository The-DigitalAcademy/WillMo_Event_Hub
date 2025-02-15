import streamlit as st
import pandas as pd
import os
from establish_connection import connect_to_database

st.set_page_config(page_title="WillMo Events Hub", layout="wide")
st.title("🎉 Welcome to WillMo Events Hub! 🎉")

# 🌟 Hero Section: Engaging Introduction
st.markdown("""
    <style>
        .hero-container {
            background-color: #FF4B4B;
            color: white;
            padding: 40px;
            text-align: center;
            border-radius: 15px;
            font-size: 22px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .hero-container h2 {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        .hero-container p {
            font-size: 1.1rem;
            margin-top: 10px;
        }
    </style>
    <div class="hero-container">
        <h2>Discover, Book, and Experience the Best Events Near You! 🚀</h2>
        <p>From concerts to business conferences, find and book events seamlessly.</p>
    </div>
""", unsafe_allow_html=True)

st.subheader("🌍 Explore Exciting Events Around You!")

# 🔎 Search Bar & Location Filter
event_title_search = st.text_input("Search for an event", "").strip()
south_african_cities = [
    "All Locations", "Cape Town", "Johannesburg", "Durban", "Pretoria", "Port Elizabeth",
    "Bloemfontein", "East London", "Polokwane", "Nelspruit", "Kimberley",
    "Pietermaritzburg", "Vanderbijlpark", "George", "Rustenburg", "Mbombela", "Tshwane"
]
location_search = st.selectbox("📍 Filter by location", south_african_cities)

# 🎭 Event Categories
st.subheader("🎟️ Browse by Category")
cols = st.columns(5)
categories = ["🎶 Concerts", "📈 Business", "⚽ Sports", "🎨 Arts & Culture", "🎤 Conferences"]
for i, category in enumerate(categories):
    cols[i].button(category)

# 🌟 Featured Events Section
st.subheader("🔥 Featured Events")

def get_upcoming_events():
    """Fetch upcoming events from the database."""
    conn = connect_to_database()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.image, l.province, l.city, e.description, e.price, e.quantity, e.event_url,
                   e.event_title, l.venue_title, e.start_date, e.start_time
            FROM "Events" as e
            LEFT JOIN "Location" as l ON l.location_id = e.location_id
            ORDER BY e.start_date ASC
            LIMIT 6;  -- Show only 6 featured events
        ''')
        events = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in events]

    except Exception as e:
        st.error(f"Error fetching events: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

events = get_upcoming_events()

if events:
    cols = st.columns(3)
    for idx, event in enumerate(events):
        col = cols[idx % 3]
        with col:
            with st.container():
                st.subheader(event['event_title'])

                image_path = event['image']
                if image_path.startswith("http"):
                    st.image(image_path, caption=event['event_title'], use_container_width=True)
                else:
                    local_image_path = f".{image_path}"
                    if os.path.exists(local_image_path):
                        st.image(local_image_path, caption=event['event_title'], use_container_width=True)
                    else:
                        st.warning(f"Image not found: {local_image_path}")

                st.write(f"📅 **Date:** {event['start_date']}")
                st.write(f"⏰ **Time:** {event['start_time']}")
                st.write(f"📍 **Location:** {event['city']}, {event['province']}")
                st.write(f"💰 **Price:** R{event['price']}")
                st.write(f"🎟️ **Tickets Left:** {event['quantity']}")



st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; text-align: center;">
        <h3>💡 Did you know?</h3>
        <p>WillMo is a South African website that allows registered users to <b>create and book events</b> with ease! 🎉</p>
        <p>Click the button below to start creating your event and bring your idea to life!</p>
        <a href="https://www.willmoeventhub.com/create-event" target="_blank">
            <button style="background-color: #FF4B4B; color: white; padding: 10px 20px; border: none; font-size: 16px; border-radius: 5px;">
                Create Your Event
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)


btn_cols = st.columns(3)
btn_cols[0].button("📅 View All Events")
btn_cols[1].button("🎟️ My Tickets")
btn_cols[2].button("📞 Contact Support")

