import streamlit as st
import json
from memory import chat_with_bot
import os
st.set_page_config(page_title="Meera", layout="wide")

def login():
    st.title("login to meera")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with open("users.json") as f:
            users = json.load(f)
        if users.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("invalid credentials")

