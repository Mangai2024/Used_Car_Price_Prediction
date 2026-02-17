import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import plotly.express as px

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host="dbmangai-1.cdig08ycykxi.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="retail_order",
        user="postgres",
        password="Rootawsroot"
    )
    return conn

# Function to execute a query and return the result as a pandas DataFrame
def run_query(query):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

# Streamlit UI
st.title("Retail Order Dashboard")

# Split queries into two sections
queries_by_guvi = {
    "Top 10 highest revenue generating products": 
       
   'SELECT t2."product_id", t2.sub_category, 
    SUM(CAST(t2."sale_price" AS FLOAT8) * CAST(t2."quantity" AS FLOAT8)) AS total_revenue
    FROM table_1 t1 
    JOIN table_2 t2 ON t1."order_id" = t2."order_id"
    GROUP BY t2."product_id", t2.sub_category
    ORDER BY total_revenue DESC
    LIMIT 10;','
}
    
    
   