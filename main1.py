import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Set page configuration first!
st.set_page_config(page_title="Orders App", page_icon="🛒", layout="centered")

# Load the model
@st.cache_resource
def load_model():
    return joblib.load("order_predictor_model.pkl")

model = load_model()
# ----- Sidebar Navigation -----
st.sidebar.title("🔧 Application Sections")
page = st.sidebar.selectbox("🧭 Go to", ["Home", "Login", "Register", "Predict Orders", "User Dashboard", "Admin Panel", "About Us"])
# ----- Page: Home -----
if page == "Home":
    st.title("🏠 Welcome to the Orders Prediction App")
    st.markdown("""
    <div style='text-align: justify;'>
    Welcome to the Orders Prediction App, your comprehensive tool to estimate the number of orders a store may receive in any given week. This app is designed to assist business owners, analysts, and data enthusiasts by providing valuable insights into the order trends of retail stores based on a range of key features.

    Retail businesses often deal with fluctuating demand based on numerous factors such as the type of store, its location, the type of discount promotions, the region in which it operates, and even the specific week of the year. Understanding these factors and predicting the volume of orders can help businesses plan better, optimize resources, and tailor their marketing efforts effectively.

    <strong>How the App Works</strong><br>
    This app uses a machine learning model to predict the number of orders a store will receive, given certain key inputs. It takes into account a combination of store-specific information and time-related features to generate accurate forecasts. The prediction model behind this app has been trained on real-world data and can provide reliable estimates for stores across various categories and regions.

    Once you enter the required data, the model processes the input and produces an estimated number of orders for the week, helping you understand how different factors influence order volume. Whether you're a store manager, a data scientist, or simply someone curious about how such predictions work, this app will serve as a helpful resource.

    <strong>Key Features for Prediction</strong><br>
    The app’s predictions are based on several key factors, which include:

    <strong>1. Store Type</strong><br>
    The Store Type refers to the category or classification of the store. Retail stores can vary significantly depending on their type, such as a supermarket, boutique, convenience store, or electronic goods store. Each type of store has its unique customer base, which can greatly influence order volume.

    Supermarkets and Large Retailers may have a consistently high number of orders each week due to their variety of products and broader customer appeal.

    Specialty or Niche Stores might experience more seasonal demand based on their product offerings.

    By selecting the appropriate store type in the app, the machine learning model can adjust its predictions to better match the characteristics of your store’s business.

    <strong>2. Location Type</strong><br>
    The Location Type specifies the kind of area where the store is situated. Store location plays a significant role in determining foot traffic and, by extension, the number of orders it will receive. For example, a store located in a city center may experience high traffic compared to one located in a rural area.

    Urban Areas often have higher demand due to the dense population and accessibility of services.

    Rural Areas, on the other hand, might experience fewer orders on average due to lower population density.

    This feature allows the app to factor in geographical and demographic trends that impact retail sales.

    <strong>3. Discount Availability</strong><br>
    Discounts and promotions are proven strategies to boost sales and increase customer engagement. In the app, you can specify whether your store offers any discounts during a particular week. The app uses this information to factor in the potential impact of discounts on order volume.

    Active Discounts generally lead to an increase in sales as customers are incentivized to make purchases.

    No Discount can often result in a more stable, but perhaps lower, number of orders.

    Discounts can significantly sway demand, especially for price-sensitive consumers.

    <strong>4. Region</strong><br>
    The Region refers to the geographical area where the store is located. This input is crucial as it helps the app account for regional trends and seasonal variations that can affect order volume. For example, a store in one region might experience higher sales due to regional festivals or holidays, while another region may have different purchasing patterns based on its cultural or economic environment.

    Different regions have unique preferences and shopping patterns, and the app considers these nuances to provide a more tailored prediction.

    <strong>5. Week Date</strong><br>
    The Week Date refers to the specific week of the year that the prediction is being made for. Week-related features such as holidays, weather, and seasonality play a huge role in influencing customer purchasing behavior.

    Holidays such as Christmas, New Year, and local festivals typically lead to an increase in orders.

    Seasonal Changes can also affect what people buy; for instance, demand for warm clothing or air conditioners may fluctuate depending on whether it's summer or winter.

    Weekend vs Weekday impacts could also be significant, with weekends generally seeing a higher number of orders.

    The app asks for the specific week start date (e.g., Monday), and from this, it calculates the relevant week number, which helps the model to understand the broader time-based trends influencing demand.

    <strong>How to Use the App</strong><br>
    Using the Orders Prediction App is simple and intuitive. Just follow these steps:

    <strong>Select Your Store Features:</strong><br>
    Choose your store type from a list of options such as supermarket, electronics, fashion, etc.

    Select the location type that best describes where your store is situated (urban, suburban, or rural).

    Choose whether there are any discounts available during the week for which you're predicting orders.

    Select the region where your store is located (the app allows you to choose from a list of regions).

    Input the start date of the week you're predicting orders for. This could be the start of any week in the year.

    <strong>View the Predicted Orders:</strong><br>
    After entering your data, the app will use its trained model to process your inputs and provide an estimated number of orders for that week. This is based on the factors you selected and how similar stores have performed in the past.

    <strong>Adjust Inputs for Accurate Predictions:</strong><br>
    You can modify any of the inputs (such as the store type, discount, or date) to see how they affect the prediction. For example, you may want to see how your orders might change if you offered a discount or if your store were located in a different region.

    <strong>Benefits of the Orders Prediction App</strong><br>
    <ul>
    <li><strong>Data-Driven Insights:</strong> The app uses data from the past to make predictions, giving you a reliable forecast based on actual trends and patterns.</li>
    <li><strong>Informed Decision-Making:</strong> Knowing the predicted number of orders helps store managers plan their inventory, staffing, and marketing strategies more effectively.</li>
    <li><strong>Customization:</strong> By allowing users to customize the inputs, the app tailors its predictions to the specific characteristics of each store, making it a valuable tool for a wide range of businesses.</li>
    </ul>

    <strong>Ideal Users of This App</strong><br>
    <ul>
    <li><strong>Store Managers:</strong> Managers can use the predictions to optimize store operations, such as inventory management, staffing, and promotions.</li>
    <li><strong>Retail Analysts:</strong> Analysts can use this app to forecast demand and plan for the future based on historical trends and other factors.</li>
    <li><strong>Business Owners:</strong> Entrepreneurs can make data-driven decisions about opening new stores, expanding operations, or offering promotions.</li>
    <li><strong>Researchers and Data Enthusiasts:</strong> Anyone interested in understanding how machine learning and data analytics can be applied in retail can benefit from using this app.</li>
    </ul>

    <strong>Conclusion</strong><br>
    The Orders Prediction App is an easy-to-use tool that leverages machine learning to give businesses accurate forecasts of order volumes based on various store features and time-related data. By understanding the influence of factors like store type, location, discounts, and week-specific trends, businesses can make informed decisions to improve their operations, increase customer satisfaction, and ultimately drive growth.

    Explore the app today and start making smarter, data-backed decisions for your retail store!
    </div>
    """, unsafe_allow_html=True)

# ----- Page: Login -----
elif page == "Login":
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":  # placeholder check
            st.success("Logged in successfully as Admin!")
        else:
            st.warning("Invalid username or password.")

# ----- Page: Register -----
elif page == "Register":
    st.title("📝 Register")
    new_user = st.text_input("Create a Username")
    new_password = st.text_input("Create a Password", type="password")
    if st.button("Register"):
        st.success("User registered successfully! (Note: No real DB connected.)")

# ----- Page: Predict Orders -----
elif page == "Predict Orders":
    st.title("🛒 Predict Number of Orders")

    st.markdown("### 📥 Input Store Data")

    store_type = st.selectbox('Store Type', [0, 1, 2, 3])
    location_type = st.selectbox('Location Type', [0, 1, 2])
    region_code = st.selectbox('Region Code', list(range(0, 53)))
    discount = st.selectbox('Discount Available?', [0, 1])
    date = st.date_input("Week Start Date", datetime(2022, 1, 1))

    # Date Features
    year = date.year
    month = date.month
    day = date.day
    week = date.isocalendar()[1]

    # Create dataframe with required features
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

# ----- Page: User Dashboard -----
elif page == "User Dashboard":
    st.title("👤 User Dashboard")
    st.markdown("""
    Welcome to your dashboard! Future functionality can include:
    - Viewing past predictions
    - Saving input history
    - Account settings
    """)

# ----- Page: Admin Panel -----
elif page == "Admin Panel":
    st.title("🛠️ Admin Panel")
    st.markdown("""
    Admin features to be implemented:
    - View user analytics
    - Manage data and models
    - Export logs and reports
    """)

# ----- Page: About Us -----
elif page == "About Us":
    st.title("ℹ️ About Us")
    st.markdown("""
    <div style='text-align: justify;'>
    
    ## 📊 About This Application

    This application, **Orders Prediction App**, is designed as a practical demonstration of integrating **Machine Learning** with **Streamlit** for real-world forecasting tasks. The app allows users to predict the number of customer orders a store might receive in a given week, based on key features like store type, region, discount availability, and date-based inputs.

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
    - Data preprocessing and feature engineering
    - Model training and evaluation (using RandomForest, XGBoost, etc.)

    ## 📬 Contact Information
    - **Email:** jeminprajapati30@gmail.com  

    ## 🎯 Objective

    The goal of this project is not only to showcase technical skills in ML and app development but also to help businesses understand how data can be used for making predictions and improving decision-making processes.

    If you'd like to collaborate or provide feedback, please reach out through the contact links above!

    ---
    <div style='text-align: center; font-size: 40px;'>
        Thank you for visiting this application! 😊
    </div>
    </div>
    """, unsafe_allow_html=True)
