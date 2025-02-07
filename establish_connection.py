import psycopg2 as ps
import pandas as pd

import streamlit as st

  # Connect to the PostgreSQL database server
connections = ps.connect(host='localhost',
                          port='5432',
                          database='willmo',
                          user= 'postgres',
                          password= '')

#Inserting data into the database

query = "SELECT * FROM willmo;"
df = pd.read_sql_query(query, connections)
connections.close()

