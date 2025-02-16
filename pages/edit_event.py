import streamlit as st
import psycopg2
from establish_connection import connect_to_database
from streamlit_extras.switch_page_button import switch_page

# Page Configuration
st.set_page_config(page_title="Manage Your Events", layout="wide")

# Establish Database Connection
conn = connect_to_database()
user_email = st.session_state.get("email", "")

st.title(" Manage Your Events")
st.subheader("Edit or delete events you have created.")

if not user_email:
    st.warning("⚠️ Please log in to manage your events.")
    st.stop()

# Fetch User's Events
if conn:
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT event_id, event_title, start_date, start_time, price FROM "Events" WHERE organizer_id IN (SELECT organizer_id FROM "Organizer" WHERE email = %s)', 
            (user_email,)
        )
        events = cursor.fetchall()

      
        if not events:
            st.info("🚀 You have not created any events yet. Start by creating one!")
            if st.button("Create an Event"):
                switch_page("creating_event")  # ✅ Redirects user to the event creation page.
            st.stop()

        # Display events in a table format
        st.write("### Your Created Events:")
        for event_id, title, date, time, price in events:
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            col1.write(f" **{title}** - {date} {time}")
            col2.write(f" **R{price}**")
            if col3.button(f"✏️ Edit", key=f"edit_{event_id}"):
                st.session_state["selected_event_id"] = event_id
                st.rerun()
            if col4.button(f"❌ Delete", key=f"delete_{event_id}"):
                st.session_state["delete_event_id"] = event_id
                st.session_state["delete_event_title"] = title
                st.rerun()

        # Handle Event Deletion
        if "delete_event_id" in st.session_state:
            delete_event_id = st.session_state["delete_event_id"]
            delete_event_title = st.session_state["delete_event_title"]
            st.warning(f"⚠️ Deleting '{delete_event_title}' will require refunding attendees.")
            if st.button("Confirm Delete", key="confirm_delete"):
                try:
                    # First, delete references in BookingEventMap
                    cursor.execute('DELETE FROM "BookingEventMap" WHERE event_id = %s', (delete_event_id,))
                    
                    # Then, delete the event itself
                    cursor.execute('DELETE FROM "Events" WHERE event_id = %s', (delete_event_id,))
                    
                    conn.commit()
                    st.success(f"✅ Event '{delete_event_title}' deleted successfully!")
                    del st.session_state["delete_event_id"]
                    del st.session_state["delete_event_title"]
                    st.rerun()
                except psycopg2.Error as e:
                    conn.rollback()
                    st.error(f"❌ Error deleting event: {e}")

        # Handle Event Editing
        if "selected_event_id" in st.session_state:
            selected_event_id = st.session_state["selected_event_id"]
            cursor.execute(
                'SELECT event_title, description, capacity, start_date, start_time, price, category_id, location_id, image FROM "Events" WHERE event_id = %s',
                (selected_event_id,)
            )
            event_details = cursor.fetchone()
            
            if event_details:
                event_title, description, capacity, start_date, start_time, price, category_id, location_id, image = event_details
                
                st.write("---")
                st.write("### ✏️ Edit Event Details")
                new_title = st.text_input("Event Title", event_title)
                new_description = st.text_area("Description", description)
                new_capacity = st.number_input("Capacity", min_value=1, value=capacity, step=1)
                new_date = st.date_input("Start Date", value=start_date)
                new_time = st.time_input("Start Time", value=start_time)
                new_price = st.number_input("Price (R)", min_value=0.0, value=price, step=0.5)
                new_image = st.text_input("Event Image URL", image)

                # Save Changes Button
                if st.button("💾 Save Changes", key="save_changes"):
                    try:
                        cursor.execute(
                            'UPDATE "Events" SET event_title = %s, description = %s, capacity = %s, start_date = %s, start_time = %s, price = %s, image = %s WHERE event_id = %s',
                            (new_title, new_description, new_capacity, new_date, new_time, new_price, new_image, selected_event_id)
                        )
                        conn.commit()
                        st.success(f"✅ Event '{new_title}' updated successfully!")
                        del st.session_state["selected_event_id"]
                        st.rerun()
                    except psycopg2.Error as e:
                        conn.rollback()
                        st.error(f"❌ Error updating event: {e}")

    except psycopg2.Error as e:
        st.error(f"Error fetching your events: {e}")
    finally:
        cursor.close()
        conn.close()
else:
    st.error("Database connection failed. Please try again later.")
