import bcrypt
import psycopg2 as ps
import streamlit as st
import re  # For email validation
from streamlit_extras.switch_page_button import switch_page

# Hide the sidebar on this page
st.set_page_config(page_title="events", page_icon=":guardsman:", layout="wide")



# Connect to the PostgreSQL database server
connection = ps.connect(
    host='localhost',
    port='5432',
    database='willmo',
    user='postgres',
    password='Will'
)

# Checking if email or contact exists in the database
def is_email_or_contact_exists(email, contact):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM "Customers" WHERE email = %s', (email,))
        email_result = cursor.fetchone()

        cursor.execute('SELECT * FROM "Customers" WHERE contact = %s', (contact,))
        contact_result = cursor.fetchone()

        return email_result is not None or contact_result is not None

# Validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Register user function
def register_user(contact, name, surname, email, password):
    with connection.cursor() as cursor:
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert user data into the "Customers" table
        cursor.execute("""
            INSERT INTO "Customers" (contact, name, surname, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (contact, name, surname, email, hashed_password))

        # Commit to save the changes
        connection.commit()

# Function to check if the login details are correct
def login_user(email, password):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM "Customers" WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            stored_password = user[4]  # because password is in the 5th column (index 4)
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                st.success("Logged in successfully!")
                st.session_state["logged_in"] = True
                st.session_state["email"] = email  # Store the user's email
                switch_page("Home")  # Redirect to home page after login
            else:
                st.error("Incorrect password!")
        else:
            st.error("User with this email not found!")

logo_path = "WillMo_Logo.jpg"
logo = st.image(logo_path, width=290)

# Use radio buttons to switch between Login and Register forms
view = st.radio("Select an option", ("Already have an account? Login", "Don't have an account? Register"))

# If the user selects "Login", show the login form
if view == "Already have an account? Login":
    st.write("### Log in to WillMo_Events_Hub")

    email = st.text_input("Email Address", placeholder="shirleymalefane0019@gmail.com")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    login_button = st.button("Log In")

    if login_button:
        if not email or not password:
            st.error("Please enter both email and password!")
        else:
            login_user(email, password)

# If the user selects "Register", show the register form
elif view == "Don't have an account? Register":
    st.write("### Register with WillMo_Events_Hub")

    with st.form("registration_form"):
        reg_email = st.text_input("Email Address", placeholder="shirleymalefane0019@gmail.com")
        name = st.text_input("Name", placeholder="Willmo")
        surname = st.text_input("Surname", placeholder="Shaper")
        contact = st.text_input("Contact", placeholder="0765712367")
        reg_password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

        terms_and_conditions = st.checkbox("I agree to the terms and conditions")

        signup_button = st.form_submit_button("Create Account")

        if signup_button:
            # Validation for all fields
            if not reg_email:
                st.error("Email Address is required!")
            elif not is_valid_email(reg_email):
                st.error("Please enter a valid email address!")
            elif not name:
                st.error("Name is required!")
            elif not surname:
                st.error("Surname is required!")
            elif not contact:
                st.error("Contact Number is required!")
            elif not contact.isdigit() or len(contact) != 10:
                st.error("Please enter a valid Contact Number.")
            elif not reg_password:
                st.error("Password is required!")
            elif len(reg_password) < 8:
                st.error("Password must have at least 8 characters.")
            elif not confirm_password:
                st.error("Confirm Password is required!")
            elif reg_password != confirm_password:
                st.error("Passwords do not match!")
            elif not terms_and_conditions:
                st.error("You must agree to the terms and conditions to register.")
            elif is_email_or_contact_exists(reg_email, contact):
                st.error("Email or Contact already exists! Please log in.")
            else:
                # Register the user if all validations pass
                register_user(contact, name, surname, reg_email, reg_password)
                st.session_state["registration_success"] = True

    if 'registration_success' in st.session_state and st.session_state.registration_success:
        st.success(f"Registration successful! Welcome, {name}.")
        st.session_state.registration_success = False
        st.session_state["logged_in"] = True  # Automatically log in the user after registration
        st.session_state["email"] = reg_email  # Store the user's email
        switch_page("Home")  # Redirect to home page after successful registration
