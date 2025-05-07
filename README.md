
# 🛒 Orders Prediction App

Welcome to the **Orders Prediction App**, a Streamlit-based machine learning web application designed to help **retail businesses**, **data analysts**, and **enthusiasts** predict the number of orders a store might receive in a given week based on several key factors.

## 🚀 Live Demo

> \[Insert your Streamlit Cloud or deployed URL here]

---

## 📌 Table of Contents

* [📌 Table of Contents](#-table-of-contents)
* [📦 Features](#-features)
* [🖥️ Screenshots](#️-screenshots)
* [📁 Project Structure](#-project-structure)
* [🔧 Installation](#-installation)
* [🧠 Model Overview](#-model-overview)
* [📊 Database Structure](#-database-structure)
* [🛠️ Admin Features](#️-admin-features)
* [👨‍💻 Developer](#-developer)
* [📃 License](#-license)

---

## 📦 Features

* 🔐 **User Authentication** (Register/Login)
* 🧮 **ML-powered Order Predictions**
* 💾 **Save & Download Predictions**
* 🧠 **Date-based Feature Engineering** (week number, month, etc.)
* 📊 **User Dashboard** for saved files and preferences
* 🛠️ **Admin Panel** for data management and user monitoring
* 📥 **CSV Upload and Download Support**
* 💌 **Email Preference Management**

---

## 🖥️ Screenshots

| Home Page                     | Predict Orders                      | User Dashboard                          | Admin Panel                     |
| ----------------------------- | ----------------------------------- | --------------------------------------- | ------------------------------- |
| ![home]("D:\sem 8\IIT Guvahati\web application\Home.png") | ![predict]("D:\sem 8\IIT Guvahati\web application\Predic order.png") | ![dashboard]("D:\sem 8\IIT Guvahati\web application\User deshboard.png") | ![admin]("D:\sem 8\IIT Guvahati\web application\Admin Panel.png") |

> *(Include screenshots in a `/screenshots` folder for GitHub preview.)*

---

## 📁 Project Structure

```bash
📦orders-prediction-app/
│
├── order_predictor_model.pkl       # Trained ML model
├── app.py                          # Main Streamlit application
├── users.db                        # SQLite DB for user data
├── orders_app.db                   # SQLite DB for prediction logs
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview
└── screenshots/                    # UI preview images
```

---

## 🔧 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/orders-prediction-app.git
cd orders-prediction-app
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the App**

```bash
streamlit run app.py
```

---

## 🧠 Model Overview

The model used for prediction is a **supervised regression model** (e.g., RandomForest or LightGBM trained offline) stored in `order_predictor_model.pkl`. It uses the following features:

* `Store_Type`, `Location_Type`, `Region_Code`
* `Discount`, `Holiday`, `Sales`
* `year`, `month`, `day`, `week`

---

## 📊 Database Structure

### SQLite Databases:

* **users.db** — Stores user login credentials.
* **user\_dashboard.db** — Stores user-uploaded CSVs and preferences.
* **orders\_app.db** — Stores all predictions made via the ML model.

Each table is created automatically at runtime if it doesn’t exist.

---

## 🛠️ Admin Features

Accessible from the **Admin Panel**:

* View all registered users
* Browse and download all prediction logs
* Monitor user uploads
* Clear predictions and uploads from the database

---

## 👨‍💻 Developer

**👤 Jemin Prajapati**
📍 Bardoli, Surat, Gujarat, India
🎓 R.N.G. Patel Institute of Technology
💼 Intern | Aspiring Data Scientist
📧 [jeminprajapati30@gmail.com](mailto:jeminprajapati30@gmail.com)

---

## 📃 License

This project is licensed under the MIT License.

