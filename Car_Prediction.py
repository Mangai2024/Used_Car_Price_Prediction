import streamlit as st
import pickle
import numpy as np
import pandas as pd
import base64
from sklearn.preprocessing import OrdinalEncoder

@st.cache_resource
# Load models
def load_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)
    
def set_background_image_local(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    base64_image = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: contain;
            background-position: fit;
            background-repeat: repeat;
            background-attachment: fixed;
        }}     
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image_local(r"12.png")


# --- Load model and encoders ---
model = load_model("car1.h5")
encoder_brand= load_model("encoder_brand.pkl")
encoder_Cities= load_model("encoder_Cities.pkl")
encoder_fuel_type = load_model("encoder_Fuel Type.pkl")
encoder_Transmission = load_model("encoder_Transmissions.pkl")
encoder_model = load_model("encoder_modell.pkl")


st.title("Car Price Prediction App")

# --- Load data to generate dropdown options ---
# Use the uploaded CSV file to create dropdown options.
df = pd.read_csv(r"finallist.csv")
# Ensure the CSV has the required columns:
# "Brand", "Fuel_Type", "Year_of_Manufacture"

dropdown_options = {
    "City": sorted(df["City"].unique().tolist()),
    "Brand": sorted(df["Brand"].unique().tolist()),
    "Fuel Type": sorted(df["Fuel Type"].unique().tolist()),
    "Transmission": sorted(df["Transmission"].unique().tolist()),
    "Model": sorted(df["Model"].unique().tolist()),
   
}

# --- Create Tabs for Home and Predict ---
tab1, tab2 = st.tabs(["Home", "Predict"])

with tab1:
    st.markdown("""
    **Welcome to the Car Price Prediction App!**

    This tool estimates car prices based on various attributes.
    
    **How it works:**
    - Navigate to the "Predict" tab.
    - Enter the car details.
    - Click "Predict" to see the estimated price.
    """)

with tab2:
    # Define columns for input layout
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col9,col10 = st.columns(2)
    
    # Categorical inputs from dropdowns
    with col1:
        City_select = st.selectbox("Select City", dropdown_options["City"])
        City_val = encoder_Cities.transform([[City_select]])[0][0]
    with col2:
        brand_select = st.selectbox("Select Brand", dropdown_options["Brand"])
        brand_val = encoder_brand.transform([[brand_select]])[0][0]
    with col3:
        fuel_type_select = st.selectbox("Select Fuel Type", dropdown_options["Fuel Type"])
        fuel_type_val = encoder_fuel_type.transform([[fuel_type_select]])[0][0]
    with col4:
        Transmission_select = st.selectbox("Select Transmission", dropdown_options["Transmission"])
        Transmission_val = encoder_Transmission.transform([[Transmission_select]])[0][0]
    with col5:
        model_select = st.selectbox("Select model", dropdown_options["Model"])
        model_val = encoder_model.transform([[model_select]])[0][0]
    
    # Numerical inputs
    with col6:
        engine_disp = st.number_input("Enter Engine Displacement (cc)", min_value=500, value=1200)
    with col7:
        mileage = st.number_input("Enter Mileage (kmpl)", min_value=5.0, value=15.0)
    with col8:
        power = st.number_input("Enter Power (bhp)", min_value=10.0, value=100.0)
    with col9:
        reg_year = st.number_input("Enter Registration Year", min_value=1900, value=2015)
    with col10:
        kms = st.number_input("Enter kms_driven", min_value=1900, value=2015)
    
    # When Predict button is clicked, compile inputs and make a prediction.
    if st.button("Predict"):
        
        
        input_data = {
            "Year of Manufacture": reg_year,
            "Kms Driven": kms,
            "Power": power,
            "Mileage": mileage,
            "Engine Displacement": engine_disp,
            "Brand": brand_val,
            "Model": model_val,
            "Transmission": Transmission_val,
            "Fuel Type": fuel_type_val,
            "City": City_val
        }
        input_df = pd.DataFrame([input_data])
        
        predicted_price = model.predict(input_df)
        st.subheader("Predicted Car Price")
        st.markdown(f"### :green[₹ {predicted_price[0]:,.2f}]")
