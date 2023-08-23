import app.db.database as db  # local import
import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import asyncio

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
import hydralit_components as hc
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import streamlit.components.v1 as components
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

from app.views.complaint import complaint
from app.views.home import home
from app.views.register import register_user
from app.views.text_predictor import text_predictor
from app.views.file_predictor import file_predictor
from app.views.report import report
from app.views.profile import profile
from app.views.reset_password import reset_password
import base64

currency = "USD"
page_title = "Sentimen Analisis Ulasan Pelanggan IndiHome"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout,initial_sidebar_state='collapsed')


def sidebar_menu(selectedNavigationSidebar, authenticator, userData): 

    if selectedNavigationSidebar == "Home": 
        # The main window
        asyncio.run(home())
        
    if selectedNavigationSidebar == "Projects":
        st.title("Projects Page")
        # The main window

    if selectedNavigationSidebar == "Keluhan":
        complaint(userData)

    if selectedNavigationSidebar == "logout":
        authenticator.logout("Logout", "main")

    if selectedNavigationSidebar == "Text Predictor":
        asyncio.run(text_predictor())

    if selectedNavigationSidebar == "File Predictor":
        file_predictor()

    if selectedNavigationSidebar == "Laporan":
        report()

    if selectedNavigationSidebar == "Account Management":
        profile()
    
    if selectedNavigationSidebar == "Logout":
        authenticator.logout("Logout", "main")

 
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
        page_bg_img = f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64.b64encode(data).decode()}");
                background-position: center -31vh;
                background-repeat: repeat;
            }}
        </style>
        """        
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    get_img_as_base64("img/background3.png")
    # --- USER AUTHENTICATION ---
    # my class function which makes a call to a database and returns a list of lists (nested list), of usernames, names, and passwords
    
    # Delete all the items in Session state
    users = db.fetch_all_users()
    # the code mentioned above
    usernames = [user['key'] for user in users]
    names = [user['name'] for user in users]
    passwords = [user['password'] for user in users]
    roles = [user['role'] for user in users]
    credentials = {"usernames":{}}

    for un, name, pw, role in zip(usernames, names, passwords, roles):
        user_dict = {"name":name,"password":pw, 'role': role}
        credentials["usernames"].update({un:user_dict})

    authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
    # name, authentication_status, username = authenticator.login("Login", "main")
    # print(authenticator.credentials)
    
    authenticator._check_cookie()
    if not st.session_state['authentication_status']:
        selected = option_menu(
            menu_title=None,
            options=["Login", "Register"],
            icons=["login", "register", "key"],  # https://icons.getbootstrap.com/
            orientation="horizontal",
        )
        if selected == "Login":
            name, authentication_status, username = authenticator.login("Login", "main")
            if authentication_status == False:
                st.error("Username/password is incorrect")
            if authentication_status == None:
                st.warning("Please enter your username and password")
        if selected == "Register":
            register_user("Register User", 'main', preauthorization=False)
        if selected == "Lupa Password":
            reset_password()
    else:
        # -------------- SETTINGS --------------
        get_user = credentials.get("usernames")[f"{st.session_state['username']}"]
        if (get_user['role'] == "admin"):
            menu_data = [
                {'id': 'Keluhan', 'icon': "💬", 'label':"Keluhan"},
                {'id': 'Text Predictor','icon':"🔮",'label':"Text Predictor"},
                {'id': 'File Predictor', 'icon': "far fa-chart-bar", 'label':"File Predictor"},#no tooltip message
                {'id': 'Laporan','icon': "📄", 'label':"Laporan"},
                {'id': 'Account Management','icon': "👤", 'label':"Account Management"}
            ]
            # sidebar_menu(["Home", "Keluhan", "Text Predictor", "File Predictor", "Laporan","Account Management"], authenticator, get_user)
        else:
            menu_data = [
                {'id': 'Keluhan', 'icon': "far fa-copy", 'label':"Keluhan"},
                {'id': 'Text Predictor','icon':"🐙",'label':"Text Predictor"},
                {'id': 'Account Management','icon': "💀", 'label':"Account Management"}
            ]
            # sidebar_menu(["Home", "Keluhan", "Text Predictor", "Account Management"], authenticator, get_user)
        selected = None
        over_theme = {'txc_inactive': '#FFFFFF'}
        menu_id = hc.nav_bar(
            menu_definition=menu_data,
            override_theme=over_theme,
            home_name='Home',
            login_name='Logout',
            hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
            sticky_nav=True, #at the top or not
            sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
        )
        with st.container():

            st.markdown("## Sentimen Analisis Ulasan Pelanggan IndiHome di PT.Telkom Indonesia 💹")
            # components.html("""<hr style="height:2px;border:none;color:#333;background-color:white;margin-bottom: 1px"/>""", height=50)
            
            # --- HIDE STREAMLIT STYLE ---
            hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        .css-1544g2n.e1fqkh3o4 {padding: 3rem 1rem 1.5rem}
                        .css-z3au9t.egzxvld2 {visibility: hidden;}  
                        button[aria-selected='true'] {padding:10px; background-color:#ff4b4b}
                        button[aria-selected='true'] p {color:#fff; font-weight:bold;}
                        button[aria-selected='true']:hover,button[aria-selected='true']:focus  {padding:10px; background-color:#910000}
                        </style>
                        """
            st.markdown(hide_st_style, unsafe_allow_html=True)
            # get_user = credentials.get("usernames")[f"{st.session_state['username']}"]
            sidebar_menu(menu_id, authenticator, get_user)
            
            # The side bar that contains radio buttons for selection of charts
            # print("===============")
            # if (get_user['role'] == "admin"):
            #     sidebar_menu(["Home", "Keluhan", "Text Predictor", "File Predictor", "Laporan","Account Management"], authenticator, get_user)
            # else:
            #     sidebar_menu(["Home", "Keluhan", "Text Predictor", "Account Management"], authenticator, get_user)

if __name__ == "__main__":
    main()
