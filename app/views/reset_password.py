import streamlit as st  # pip install streamlit
import app.db.database as db  # local import
import streamlit_authenticator as stauth

def reset_password():
    st.write("Reset Password")
    
    username = st.text_input("Username: ")
    password = st.text_input("Password: ", type='password')
    if (password != ""):
        password = stauth.Hasher([password]).generate()[0]
    else:
        st.error("Maaf password mohon diisi")

    if (st.button("Submit")):
        user = db.get_username(username)
        if (user == None):
            st.error("Maaf user tidak ditemukan")
            return
        
        data = {
            "password":password,
        }
        db.update_user(data, username)
        st.success(f"Success Update")
        # st.experimental_rerun()

