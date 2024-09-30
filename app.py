import streamlit as st
import hashlib
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["karthik"]
collection = db["collection"]

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup function
def signup(username, password):
    try:
        if collection.find_one({"username": username}):
            st.error("Username already exists!")
        else:
            hashed_pwd = hash_password(password)
            collection.insert_one({"username": username, "password": hashed_pwd})
            st.success("Signup successful! Please log in.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Login function
def login(username, password):
    try:
        user = collection.find_one({"username": username})
        if user and user["password"] == hash_password(password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Auth page
def auth_page():
    st.title("Login / Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            login(username, password)
    with col2:
        if st.button("Signup"):
            signup(username, password)

# Dashboard page
def dashboard():
    st.title("Dashboard")
    st.write(f"Welcome, {st.session_state['username']}!")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

# Main app
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        dashboard()
    else:
        auth_page()

if __name__ == "__main__":
    main()
