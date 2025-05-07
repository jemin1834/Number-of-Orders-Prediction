import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Set page configuration with centered layout
st.set_page_config(page_title="Orders App", page_icon="🛒", layout="centered")

# Load the model
@st.cache_resource
def load_model():
    return joblib.load("order_predictor_model.pkl")

model = load_model()

# ----- Sidebar Navigation -----
st.sidebar.title("🔧 Application Sections")
page = st.sidebar.selectbox("🧭 Go to", ["Home", "Login", "Register", "Predict Orders", "User Dashboard", "Admin Panel", "About Us"])

# ----- Page Content -----
if page == "Home":
    st.title("🏠 Welcome to the Orders Prediction App")
    st.markdown("""
    <div style='text-align: justify;'>
    Welcome to the Orders Prediction App, your comprehensive tool to estimate the number of orders a store may receive in any given week. This app is designed to assist business owners, analysts, and data enthusiasts by providing valuable insights into the order trends of retail stores based on a range of key features.

    Retail businesses often deal with fluctuating demand based on numerous factors such as the type of store, its location, the type of discount promotions, the region in which it operates, and even the specific week of the year. Understanding these factors and predicting the volume of orders can help businesses plan better, optimize resources, and tailor their marketing efforts effectively.
    </div>
    """, unsafe_allow_html=True)

elif page == "Login":
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.success("Logged in successfully as Admin!")
        else:
            st.warning("Invalid username or password.")

elif page == "Register":
    st.title("📝 Register")
    new_user = st.text_input("Create a Username")
    new_password = st.text_input("Create a Password", type="password")
    if st.button("Register"):
        st.success("User registered successfully! (Note: No real DB connected.)")

elif page == "Predict Orders":
    st.title("🛒 Predict Number of Orders")
    store_type = st.selectbox('Store Type', [0, 1, 2, 3])
    location_type = st.selectbox('Location Type', [0, 1, 2])
    region_code = st.selectbox('Region Code', list(range(0, 53)))
    discount = st.selectbox('Discount Available?', [0, 1])
    date = st.date_input("Week Start Date", datetime(2022, 1, 1))

    year = date.year
    month = date.month
    day = date.day
    week = date.isocalendar()[1]

    input_data = pd.DataFrame({
        'Store_id': [0],
        'Store_Type': [store_type],
        'Location_Type': [location_type],
        'Region_Code': [region_code],
        'Holiday': [0],
        'Discount': [discount],
        'Sales': [0],
        'year': [year],
        'month': [month],
        'day': [day],
        'week': [week]
    })

    st.write("📄 Input Data", input_data)

    if st.button("Predict Orders"):
        prediction = model.predict(input_data)
        st.success(f"📈 Estimated Orders: {int(prediction[0])}")

elif page == "User Dashboard":
    st.title("👤 User Dashboard")
    st.markdown("""Welcome to your dashboard! Future functionality can include:
    - Viewing past predictions
    - Saving input history
    - Account settings
    """)

elif page == "Admin Panel":
    st.title("🛠️ Admin Panel")
    st.markdown("""Admin features to be implemented:
    - View user analytics
    - Manage data and models
    - Export logs and reports
    """)

elif page == "About Us":
    st.title("ℹ️ About Us")
    st.markdown("""
    <div style='text-align: justify;'>

    ## 📊 About This Application

    This application, **Orders Prediction App**, is designed as a practical demonstration of integrating **Machine Learning** with **Streamlit** for real-world forecasting tasks.

    ## 👨‍💻 Developer Profile

    **Name:** Jemin Prajapati  
    **Profession:** Aspiring Data Scientist / Machine Learning Enthusiast  
    **Education:** R.N.G PATEL INSTITUTE OF TECHNOLOGY, B.Tech in Computer Science and Engineering honor of a Specialization in AL and ML  
    **Current Role:** Intern  
    **Location:** Bardoli, Surat, Gujarat, India  

    ## 🧠 Skills & Technologies Used
    - Python 🐍
    - Machine Learning (scikit-learn, pandas, NumPy)
    - Streamlit (for building the web interface)

    ## 📬 Contact Information
    - **Email:** jeminprajapati30@gmail.com  

    ## 🎯 Objective

    The goal of this project is not only to showcase technical skills in ML and app development but also to help businesses understand how data can be used for making predictions and improving decision-making processes.

    </div>
    """, unsafe_allow_html=True)
