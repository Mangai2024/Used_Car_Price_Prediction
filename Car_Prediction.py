import streamlit as st
import pandas as pd
import pickle
import base64

# --- Helper functions ---
@st.cache_resource
def load_model(model_path):
    with open(model_path, "rb") as f:
        return pickle.load(f)

def set_background_image_local(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    base64_img = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --- Load model and encoders ---
model = load_model("random_forest_model.pkl")
encoder_area = load_model("Area.pkl")
encoder_brand = load_model("Brand.pkl")
encoder_engine_disp = load_model("Engine_Displacement_(cc).pkl")
encoder_fuel_type = load_model("Fuel_Type.pkl")
encoder_mileage = load_model("Mileage_(kmpl).pkl")
encoder_power = load_model("Power_(bhp).pkl")
encoder_reg_year = load_model("Registration_Year.pkl")
encoder_yom = load_model("Year_of_Manufacture.pkl")

st.title("Car Price Prediction App")

# --- Load data to generate dropdown options ---
# Use the uploaded CSV file to create dropdown options.
selected_df = pd.read_csv(r"E:\Used_Car_Price_Prediction\Final_UsedCars _Datafile.csv")
# Ensure the CSV has the required columns:
# "Area", "Brand", "Fuel_Type", "Year_of_Manufacture"
dropdown_options = {
    "Area": sorted(df["Area"].unique().tolist()),
    "Brand": sorted(df["Brand"].unique().tolist()),
    "Fuel_Type": sorted(df["Fuel_Type"].unique().tolist()),
    "Year_of_Manufacture": sorted(df["Year_of_Manufacture"].unique().tolist())
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
    
    # Categorical inputs from dropdowns
    with col1:
        area_select = st.selectbox("Select Area", dropdown_options["Area"])
        area_val = encoder_area.transform([[area_select]])[0][0]
    with col2:
        brand_select = st.selectbox("Select Brand", dropdown_options["Brand"])
        brand_val = encoder_brand.transform([[brand_select]])[0][0]
    with col3:
        fuel_type_select = st.selectbox("Select Fuel Type", dropdown_options["Fuel_Type"])
        fuel_type_val = encoder_fuel_type.transform([[fuel_type_select]])[0][0]
    with col4:
        yom_select = st.selectbox("Select Year of Manufacture", dropdown_options["Year_of_Manufacture"])
        yom_val = encoder_yom.transform([[yom_select]])[0][0]
    
    # Numerical inputs
    with col5:
        engine_disp = st.number_input("Enter Engine Displacement (cc)", min_value=500, value=1200)
    with col6:
        mileage = st.number_input("Enter Mileage (kmpl)", min_value=5.0, value=15.0)
    with col7:
        power = st.number_input("Enter Power (bhp)", min_value=10.0, value=100.0)
    with col8:
        reg_year = st.number_input("Enter Registration Year", min_value=1900, value=2015)
    
    # When Predict button is clicked, compile inputs and make a prediction.
    if st.button("Predict"):
        # Transform numerical inputs using encoders (if available) or use directly.
        engine_disp_val = encoder_engine_disp.transform([[engine_disp]])[0][0]
        mileage_val = encoder_mileage.transform([[mileage]])[0][0]
        power_val = encoder_power.transform([[power]])[0][0]
        reg_year_val = encoder_reg_year.transform([[reg_year]])[0][0]
        
        input_data = {
            "Area": area_val,
            "Brand": brand_val,
            "Engine_Displacement_(cc)": engine_disp_val,
            "Fuel_Type": fuel_type_val,
            "Mileage_(kmpl)": mileage_val,
            "Power_(bhp)": power_val,
            "Registration_Year": reg_year_val,
            "Year_of_Manufacture": yom_val
        }
        input_df = pd.DataFrame([input_data])
        
        predicted_price = model.predict(input_df)
        st.subheader("Predicted Car Price")
        st.markdown(f"### :green[₹ {predicted_price[0]:,.2f}]")
