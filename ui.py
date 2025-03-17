import streamlit as st
import requests
import pandas as pd

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/products/"

st.set_page_config(page_title="Product Dashboard", layout="wide")

st.title("🛍️ Product Dashboard")

# Fetch data from FastAPI
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Display products in a table
        st.write("### Product List")
        st.dataframe(df, use_container_width=True)

        # Add Filters
        category = st.selectbox("Filter by Category", options=["All"] + list(df["category"].unique()))
        if category != "All":
            df = df[df["category"] == category]

        # Display Filtered Data
        st.write("### Filtered Products")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Failed to fetch data from API. Check if FastAPI is running.")
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the FastAPI server. Make sure it's running.")
