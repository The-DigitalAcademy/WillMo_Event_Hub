import psycopg2 as ps
import pandas as pd

import streamlit as st

def connect_to_database():
    try:
        connection = ps.connect(
            host='localhost',
            port='5432',
            database='willmo',
            user='postgres',
            password=''
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")