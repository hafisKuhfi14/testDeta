import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import asyncio

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import streamlit.components.v1 as components
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

import pandas as pd
import plotly.express as px
import database as db  # local import
import ast
from app import page

incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]
currency = "USD"
page_title = "Sentimen Analisis Ulasan Pelanggan IndiHome"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# --- USER AUTHENTICATION ---
# my class function which makes a call to a database and returns a list of lists (nested list), of usernames, names, and passwords
users = db.fetch_all_users()
# the code mentioned above
usernames = [user['key'] for user in users]
names = [user['name'] for user in users]
passwords = [user['password'] for user in users]
username = ""

credentials = {"usernames":{}}

for un, name, pw in zip(usernames, names, passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
# name, authentication_status, username = authenticator.login("Login", "main")
# print(authenticator.credentials)

authenticator._check_cookie()
if not st.session_state['authentication_status']: 
    print("Masuk IF")
    selected = option_menu(
        menu_title=None,
        options=["Login", "Register"],
        icons=["login", "register"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )
    if selected == "Login":
        name, authentication_status, username = authenticator.login("Login", "main")
        if authentication_status == False:
            st.error("Username/password is incorrect")
        if authentication_status == None:
            st.warning("Please enter your username and password")
    if selected == "Register":
        page.register_user("Register User", 'main', preauthorization=False)
else:
    # -------------- SETTINGS --------------
    selected = None

    st.markdown("## Sentimen Analisis Ulasan Pelanggan IndiHome di PT.Telkom Indonesia 💹")
    components.html("""<hr style="height:2px;border:none;color:#333;background-color:white;margin-bottom: 1px"/>""", height=50)

    # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
    years = [datetime.today().year, datetime.today().year + 1]
    months = list(calendar.month_name[1:])

    # --- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                .css-1544g2n.e1fqkh3o4 {padding: 3rem 1rem 1.5rem}
                .css-z3au9t.egzxvld2 {visibility: hidden;}  
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Code to import libraries and get the data goes here

    # The side bar that contains radio buttons for selection of charts
    with st.sidebar:
        st.markdown(f'# Selamat Datang {name}')
        selectedNavigationSidebar = option_menu(
            menu_title=None,
            options=["Home", "Projects", "Keluhan", "Text Predictor"],
            icons=["house", "book", "chat", "fonts"],
            menu_icon="cast",
            default_index=0,
        )
        authenticator.logout("Logout", "main")

    if selectedNavigationSidebar == "Home": 
        # The main window
        page.home()
        
    if selectedNavigationSidebar == "Projects":
        st.title("Projects Page")
        # The main window

    if selectedNavigationSidebar == "Keluhan":
        page.complaint(username)

    if selectedNavigationSidebar == "logout":
        authenticator.logout("Logout", "main")

    if selectedNavigationSidebar == "Text Predictor":
        asyncio.run(page.text_predictor())

# async def main():
#     users = db.fetch_all_users()
#     usernames = [user['key'] for user in users]
#     names = [user['name'] for user in users]
#     passwords = [user['password'] for user in users]
#     print(names)
#     username = ""
#     credentials = {"usernames":{}}

# if __name__ == "__main__":
#     asyncio.run(main())