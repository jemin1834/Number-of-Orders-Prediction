import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import sqlite3

# ----- DATABASE SETUP -----
# Connect to SQLite DB
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
# Establish connection to SQLite DB (or create it)
conn = sqlite3.connect('user_dashboard.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    data TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    notifications INTEGER,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')
conn.commit()

# ----- MODEL LOADING -----
@st.cache_resource
def load_model():
    return joblib.load("order_predictor_model.pkl")

model = load_model()

# 🔧 MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Orders App", page_icon="🛒", layout="wide")

# ----- SIDEBAR NAVIGATION -----
st.sidebar.title("🔧 Application Sections")
page = st.sidebar.selectbox("🧭 Go to", ["Home", "Login", "Register", "Predict Orders", "User Dashboard", "Admin Panel", "About Us"])

# ----- PAGE CONTENT -----

if page == "Home":
    st.title("🏠 Welcome to the Orders Prediction App")
    st.markdown("""
<div style='text-align: justify; font-size: 20px;'>
    📊 <strong>Welcome to the Orders Prediction App</strong>, your comprehensive tool to estimate the number of orders a store may receive in any given week. This app is designed to assist <span style="color:#2E86C1;"><strong>business owners</strong></span>, <span style="color:#28B463;"><strong>analysts</strong></span>, and <span style="color:#CA6F1E;"><strong>data enthusiasts</strong></span> by providing valuable insights into the order trends of retail stores based on a range of key features.<br><br>

    🏬 Retail businesses often deal with fluctuating demand based on numerous factors such as:
    ✅ the type of store
    📍 its location
    🧾 discount promotions
    🌍 region of operation
    📅 and even the specific week of the year

    📦 Understanding these factors and predicting the volume of orders can help businesses:
    🔧 plan better
    ⚙️ optimize resources
    🎯 and tailor marketing efforts effectively.
</div>
"""
, unsafe_allow_html=True)

elif page == "Login":
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if cursor.fetchone():
            st.success(f"✅ Logged in successfully as {username}!")
        else:
            st.warning("❌ Invalid username or password.")

elif page == "Register":
    st.title("📝 Register")
    new_user = st.text_input("Create a Username")
    new_password = st.text_input("Create a Password", type="password")
    if st.button("Register"):
        cursor.execute("SELECT * FROM users WHERE username = ?", (new_user,))
        if cursor.fetchone():
            st.warning("🚫 Username already exists. Please choose another.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, new_password))
            conn.commit()
            st.success("✅ User registered successfully!")

elif page == "Predict Orders":
    st.title("🛒 Predict Number of Orders")

    # User Input
    store_type = st.selectbox('Store Type', [0, 1, 2, 3])
    location_type = st.selectbox('Location Type', [0, 1, 2])
    region_code = st.selectbox('Region Code', list(range(0, 53)))
    discount = st.selectbox('Discount Available?', [0, 1])
    date = st.date_input("Week Start Date", datetime(2022, 1, 1))

    # Extract date parts
    year = date.year
    month = date.month
    day = date.day
    week = date.isocalendar()[1]

    # Prepare input
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

    # Predict and Save
    if st.button("Predict Orders"):
        prediction = model.predict(input_data)
        predicted_orders = int(prediction[0])
        st.success(f"📈 Estimated Orders: {predicted_orders}")

        # Ensure table exists
        conn = sqlite3.connect("orders_app.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Predictions (
                Store_id INTEGER,
                Store_Type INTEGER,
                Location_Type INTEGER,
                Region_Code INTEGER,
                Holiday INTEGER,
                Discount INTEGER,
                Sales INTEGER,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                week INTEGER,
                Predicted_Orders INTEGER,
                Prediction_Timestamp TEXT
            );
        """)
        conn.commit()

        # Save prediction to DB
        input_data['Predicted_Orders'] = predicted_orders
        input_data['Prediction_Timestamp'] = datetime.now()
        input_data.to_sql("Predictions", conn, if_exists='append', index=False)
        conn.close()
        st.success("✅ Prediction saved to database.")

        # CSV download
        csv = input_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Prediction as CSV",
            data=csv,
            file_name='order_prediction.csv',
            mime='text/csv',
        )

    # Show recent predictions
    try:
        with sqlite3.connect("orders_app.db") as conn:
            df = pd.read_sql(
                "SELECT * FROM Predictions ORDER BY Prediction_Timestamp DESC LIMIT 5", conn)
            if not df.empty:
                st.subheader("🕓 Recent Predictions")
                st.dataframe(df)
            else:
                st.info("No past predictions found.")
    except Exception as e:
        st.error(f"Error fetching previous predictions: {e}")


elif page == "User Dashboard":
    st.title("👤 User Dashboard")
    st.markdown("Welcome to your dashboard!")

    # Username simulation (hardcoded for now)
    username = "jemin"

    # Section 1: Upload and Save Previous Predictions
    st.subheader("📤 Upload Previous Predictions")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(data)

        if st.button("Save to Database"):
            data_str = data.to_json()
            cursor.execute("INSERT INTO predictions (username, data) VALUES (?, ?)", (username, data_str))
            conn.commit()
            st.success("Data saved to database!")

    # Section 2: View Saved Predictions
    st.subheader("📑 View Saved Prediction Data")
    cursor.execute("SELECT data, uploaded_at FROM predictions WHERE username = ? ORDER BY uploaded_at DESC", (username,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            st.markdown(f"**Uploaded at:** {row[1]}")
            df = pd.read_json(row[0])
            st.dataframe(df)
    else:
        st.info("No saved data yet. Upload above to get started.")

    # Section 3: User Preferences
    st.subheader("⚙️ User Preferences")
    notif = st.checkbox("Enable Email Notifications", value=True)
    email = st.text_input("Update Email", value="jeminprajapati30@gmail.com")

    if st.button("Save Preferences"):
        cursor.execute("INSERT INTO preferences (username, email, notifications) VALUES (?, ?, ?)", (username, email, int(notif)))
        conn.commit()
        st.success("Preferences saved to database!")

elif page == "Admin Panel":
    st.title("🛠️ Admin Panel")
    st.markdown("Manage users, monitor predictions, and export data.")

    st.subheader("👥 Registered Users")
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    if users:
        st.table(pd.DataFrame(users, columns=["Username"]))
    else:
        st.info("No registered users yet.")

    st.subheader("📈 Prediction Logs")
    with sqlite3.connect("orders_app.db") as conn:
        pred_df = pd.read_sql("SELECT * FROM Predictions ORDER BY Prediction_Timestamp DESC", conn)
        if not pred_df.empty:
            st.dataframe(pred_df)
            csv_data = pred_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download All Predictions (CSV)",
                data=csv_data,
                file_name="all_predictions.csv",
                mime="text/csv"
            )
        else:
            st.info("No predictions recorded yet.")

    st.subheader("🗂️ Uploaded User Files")
    cursor.execute("SELECT username, uploaded_at FROM predictions")
    uploads = cursor.fetchall()
    if uploads:
        st.table(pd.DataFrame(uploads, columns=["Username", "Uploaded At"]))
    else:
        st.info("No uploaded files by users yet.")

    st.subheader("⚙️ Maintenance Options")
    if st.button("🧹 Clear All Predictions"):
        with sqlite3.connect("orders_app.db") as conn:
            conn.execute("DELETE FROM Predictions")
            conn.commit()
        st.success("All predictions cleared.")

    if st.button("🧹 Clear User Uploads"):
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        st.success("All uploaded data cleared.")

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
