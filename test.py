import streamlit as st
import psycopg2
from datetime import datetime

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

# Add event to cart
def add_to_cart(email, event_id, quantity):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "Cart" (email, event_id, user_quantity)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (email, event_id) DO UPDATE 
                    SET user_quantity = user_quantity + EXCLUDED.user_quantity;
                """, (email, event_id, quantity))
                conn.commit()
        except Exception as e:
            st.error(f"Error adding to cart: {e}")
        finally:
            conn.close()

# Delete event from cart
def delete_from_cart(cart_id):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM "Cart" WHERE cart_id = %s;
                """, (cart_id,))
                conn.commit()
        except Exception as e:
            st.error(f"Error deleting from cart: {e}")
        finally:
            conn.close()

# Update quantity in cart
def update_cart_quantity(cart_id, new_quantity):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE "Cart" SET user_quantity = %s WHERE cart_id = %s;
                """, (new_quantity, cart_id))
                conn.commit()
        except Exception as e:
            st.error(f"Error updating cart: {e}")
        finally:
            conn.close()

# Confirm and pay (update booking status and remove items from cart)
def confirm_and_pay(email):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Get cart items for the user
                cursor.execute("""
                    SELECT c.cart_id, c.event_id, c.user_quantity, e.price 
                    FROM "Cart" c
                    JOIN "Events" e ON c.event_id = e.event_id
                    WHERE c.email = %s
                """, (email,))
                cart_items = cursor.fetchall()

                # Add bookings and update status to 'confirmed'
                for item in cart_items:
                    cart_id, event_id, quantity, price = item
                    cursor.execute("""
                        INSERT INTO "Bookings" (email, event_id, status) 
                        VALUES (%s, %s, 'confirmed');
                    """, (email, event_id))

                # Remove items from cart after payment
                cursor.execute("""
                    DELETE FROM "Cart" WHERE email = %s;
                """, (email,))
                conn.commit()

                # Display success message
                st.success("Your booking has been confirmed!")
                st.session_state["page"] = "events"  # Redirect to events page
                st.experimental_rerun()

        except Exception as e:
            st.error(f"Error processing payment: {e}")
        finally:
            conn.close()

# Cart Page
def display_cart_page():
    # Check if the user is logged in
    email = st.session_state.get("email")
    if not email:
        st.warning("You must be logged in to view your cart.")
        st.session_state["page"] = "register"  # Redirect to the register page
        st.experimental_rerun()

    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Fetch cart items for the logged-in user
                cursor.execute("""
                    SELECT c.cart_id, c.event_id, e.event_title, c.user_quantity, e.price, e.image
                    FROM "Cart" c
                    JOIN "Events" e ON c.event_id = e.event_id
                    WHERE c.email = %s
                """, (email,))
                cart_items = cursor.fetchall()

                if not cart_items:
                    st.write("Your cart is empty.")
                    return

                st.header("Your Cart")

                total_price = 0
                for item in cart_items:
                    cart_id, event_id, event_title, quantity, price, image = item
                    subtotal = quantity * price
                    total_price += subtotal

                    # Display cart item with small image, quantity, and price
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        st.image(image, width=50) 
                    with col2:
                        st.write(f"**{event_title}**")
                        st.write(f"**Quantity:** {quantity}")
                        st.write(f"**Price:** R{price}")
                        st.write(f"**Subtotal:** R{subtotal}")
                    with col3:
                        delete_button = st.button(f"Delete", key=f"delete_{cart_id}")
                        if delete_button:
                            delete_from_cart(cart_id)
                            st.experimental_rerun()  # Refresh page after deletion

                st.write(f"**Total Price:** R{total_price}")

                # Button to proceed to payment
                if st.button("Pay Now"):
                    confirm_and_pay(email)

        except Exception as e:
            st.error(f"Error loading cart: {e}")
        finally:
            conn.close()
