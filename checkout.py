import streamlit as st
import psycopg2

# Helper function to connect to the database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db",
            user="your_user",
            password="your_password"
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Fetch the cart count for the logged-in user
def fetch_cart_count(email):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM "Cart" WHERE email = %s;
                """, (email,))
                count = cursor.fetchone()[0]
                return count
        except Exception as e:
            st.error(f"Error fetching cart count: {e}")
        finally:
            conn.close()
    return 0

# Display cart icon in the sidebar
def display_cart_icon():
    email = st.session_state.get("email")
    if not email:
        # If not logged in, display a default cart with no badge
        st.sidebar.write("🛒 Cart")
        return
    
    # Fetch cart count for logged-in user
    cart_count = fetch_cart_count(email)
    
    # Display the cart icon with a badge showing the count
    if cart_count > 0:
        st.sidebar.markdown(f"**🛒 Cart ({cart_count})**")
    else:
        st.sidebar.markdown("**🛒 Cart**")
    
    # Add a button to navigate to the cart page
    if st.sidebar.button("View Cart"):
        st.session_state["page"] = "cart"
        st.experimental_rerun()

# Cart Page Placeholder
def display_cart_page():
    st.title("Your Cart")
    st.write("Cart page content goes here.")
    # Add your cart logic here...

# Main Application Logic
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# Sidebar with cart icon
display_cart_icon()

# Navigation Logic
if st.session_state["page"] == "landing":
    st.title("Landing Page")
    st.write("Welcome to the Event Booking System!")
elif st.session_state["page"] == "cart":
    display_cart_page()
