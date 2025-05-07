import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import sqlite3

# ----- DATABASE SETUP -----
conn = sqlite3.connect('user_dashboard.db', check_same_thread=False)
cursor = conn.cursor()

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

# ----- SESSION STATE -----
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# ----- PAGE CONFIG -----
# MUST be the first Streamlit command
st.set_page_config(page_title="Orders App", page_icon="🛒", layout="wide")


# ----- SIDEBAR NAVIGATION -----
if not st.session_state.logged_in:
    page = st.sidebar.selectbox("🔐 Authentication", ["Login", "Register"])
else:
    page = st.sidebar.selectbox("🧭 Go to", ["Home", "Predict Orders", "User Dashboard", "Admin Panel", "About Us", "Logout"])

# ----- LOGIN / REGISTER -----
if page == "Login":
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if cursor.fetchone():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Logged in successfully as {username}!")
            st.rerun()
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

# ----- MAIN APP AFTER LOGIN -----
elif page == "Home":
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
""", unsafe_allow_html=True)

elif page == "Predict Orders":
    st.title("🛒 Predict Number of Orders")
    store_type = st.selectbox('Store Type', [0, 1, 2, 3])
    location_type = st.selectbox('Location Type', [0, 1, 2])
    region_code = st.selectbox('Region Code', list(range(0, 53)))
    discount = st.selectbox('Discount Available?', [0,1])
    date = st.date_input("Week Start Date", datetime(2022, 1, 1))
    year, month, day, week = date.year, date.month, date.day, date.isocalendar()[1]
    
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
        predicted_orders = int(prediction[0])
        st.success(f"📈 Estimated Orders: {predicted_orders}")
        input_data['Predicted_Orders'] = predicted_orders
        input_data['Prediction_Timestamp'] = datetime.now()

        with sqlite3.connect("orders_app.db") as conn2:
            conn2.execute("""
    CREATE TABLE IF NOT EXISTS Predictions(
        Store_id INTEGER,
        Date TEXT,
        Item_id INTEGER,
        Predicted_Quantity INTEGER,
        Prediction_Timestamp TEXT
    );
""")
 # fill as per original
            input_data.to_sql("Predictions", conn2, if_exists='append', index=False)

        st.success("✅ Prediction saved to database.")
        csv = input_data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Prediction as CSV", csv, "order_prediction.csv", "text/csv")

        try:
            with sqlite3.connect("orders_app.db") as conn2:
                df = pd.read_sql("SELECT * FROM Predictions ORDER BY Prediction_Timestamp DESC LIMIT 5", conn2)
                if not df.empty:
                    st.subheader("🕓 Recent Predictions")
                    st.dataframe(df)
        except Exception as e:
            st.error(f"Error fetching previous predictions: {e}")

elif page == "User Dashboard":
    st.title("👤 User Dashboard")
    st.markdown("Welcome to your dashboard!")
    username = st.session_state.username

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

    st.subheader("📑 View Saved Prediction Data")
    cursor.execute("SELECT data, uploaded_at FROM predictions WHERE username = ? ORDER BY uploaded_at DESC", (username,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            st.markdown(f"**Uploaded at:** {row[1]}")
            df = pd.read_json(row[0])
            st.dataframe(df)
    else:
        st.info("No saved data yet.")

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
    st.table(pd.DataFrame(users, columns=["Username"]))

    st.subheader("📈 Prediction Logs")
    with sqlite3.connect("orders_app.db") as conn2:
        pred_df = pd.read_sql("SELECT * FROM Predictions ORDER BY Prediction_Timestamp DESC", conn2)
        st.dataframe(pred_df)
        csv_data = pred_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download All Predictions (CSV)", csv_data, "all_predictions.csv", "text/csv")

    st.subheader("🗂️ Uploaded User Files")
    cursor.execute("SELECT username, uploaded_at FROM predictions")
    uploads = cursor.fetchall()
    st.table(pd.DataFrame(uploads, columns=["Username", "Uploaded At"]))

    st.subheader("⚙️ Maintenance Options")
    if st.button("🧹 Clear All Predictions"):
        with sqlite3.connect("orders_app.db") as conn2:
            conn2.execute("DELETE FROM Predictions")
            conn2.commit()
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

elif page == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("🔒 Logged out successfully!")
    st.experimental_rerun()
