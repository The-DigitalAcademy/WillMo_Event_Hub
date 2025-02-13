import streamlit as st
import pandas as pd
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page

def fetch_events(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        if not result:
            return pd.DataFrame()
        columns = ["event_id", "event_title", "image", "start_date", "start_time", "price", "quantity", "category", "city", "province"]
        events_df = pd.DataFrame(result, columns=columns)
        return events_df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# CSS for styling the cards
st.markdown(
    """
    <style>
    .card-title {
        font-size: 16px;
        font-weight: bold;
        margin: 10px 0;
    }
    .card-details {
        font-size: 14px;
        color: #666;
    }
    .card-price {
        font-size: 14px;
        font-weight: bold;
        margin: 10px 0;
        color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def display_booking_page():
    st.subheader("Search and Filter Events")
    search_query = st.text_input("Search events by name:", placeholder="Enter event name")
    selected_date = st.date_input("Select Date", value=None)
    category = st.multiselect(
        "Category",
        ["All", "Charity Event", "Fashion Event", "Festival", "Art Event", 
         "Social Event", "Sports", "Online Event", "Hybrid Event"]
    )
    province = st.multiselect(
        "Province",
        ["All", "Gauteng", "KwaZulu-Natal", "Eastern Cape", "Free State", 
         "Western Cape", "Northern Cape", "North West", "Mpumalanga", "Limpopo"]
    )

    connection = connect_to_database()
    if not connection:
        st.error("Database connection failed.")
        return

    filters = []
    if search_query:
        filters.append(("e.event_title ILIKE %s", f"%{search_query}%"))
    if selected_date:
        filters.append(("e.start_date = %s", selected_date))
    if category and "All" not in category:
        filters.append(("LOWER(c.category) IN %s", tuple([cat.lower() for cat in category])))
    if province and "All" not in province:
        filters.append(("l.province IN %s", tuple(province)))

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

    events = fetch_events(connection, query, list(params))

    if not events.empty:
        st.write(f"Found {len(events)} events:")
    else:
        st.info("No events match your search criteria. Showing related events instead.")

        fallback_query = """
            SELECT e.event_id, e.event_title, e.image, e.start_date, e.start_time, e.price, e.quantity,
                   c.category, l.city, l.province
            FROM "Events" e
            INNER JOIN "Category" c ON e.category_id = c.category_id
            INNER JOIN "Location" l ON e.location_id = l.location_id
            WHERE {category_clause} {province_clause} e.start_date >= CURRENT_DATE
            LIMIT 10
        """

        category_clause = "c.category IN %s AND " if category else ""
        province_clause = "l.province IN %s AND " if province else ""

        fallback_query = fallback_query.format(
            category_clause=category_clause,
            province_clause=province_clause
        )

        fallback_params = []
        if category:
            fallback_params.append(tuple(category))
        if province:
            fallback_params.append(tuple(province))

        events = fetch_events(connection, fallback_query, fallback_params)

    for i in range(0, len(events), 3):
        row_events = events.iloc[i:i + 3]
        cols = st.columns(3, gap="large")
        for col, (_, event) in zip(cols, row_events.iterrows()):
            with col:
                with st.container():
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.image(event["image"], use_column_width=True, caption=None)
                    st.markdown(f'<div class="card-title">{event["event_title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Date: {event["start_date"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Time: {event["start_time"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Category: {event["category"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">Province: {event["province"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-details">City: {event["city"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-price">Price: R{event["price"]}</div>', unsafe_allow_html=True)
                    if st.button("More Details", key=f"details_{event['event_id']}"):
                        st.session_state["event_id"] = event["event_id"]
                        switch_page("event_details")
                    st.markdown('</div>', unsafe_allow_html=True)

display_booking_page()
