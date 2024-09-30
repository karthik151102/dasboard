import streamlit as st
import hashlib
from pymongo import MongoClient
import webbrowser

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["karthik"]
collection = db["collection"]

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup function
def signup(username, password):
    if collection.find_one({"username": username}):
        st.error("Username already exists!")
    else:
        hashed_pwd = hash_password(password)
        collection.insert_one({"username": username, "password": hashed_pwd})
        st.success("Signup successful! Please log in.")

# Login function
def login(username, password):
    user = collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(f"Welcome {username}!")
        url = "http://localhost:8501/dashboard"
        webbrowser.open_new_tab(url)
    else:
        st.error("Invalid username or password.")

# Auth page
def auth_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)
    if st.button("Signup"):
        signup(username, password)

# Main app
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.write("You are logged in.")
    else:
        auth_page()