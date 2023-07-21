import app.db.database as db  # local import
import streamlit_authenticator as stauth
import streamlit as st  # pip install streamlit

def register_user(form_name: str, location: str='main', preauthorization=True) -> bool:
    if location == 'main':
        register_user_form = st.form('Register user')

    register_user_form.subheader(form_name)
    new_username = register_user_form.text_input('Username').lower()
    new_name = register_user_form.text_input('Name')
    new_password = register_user_form.text_input('Password', type='password')
    new_password_repeat = register_user_form.text_input('Repeat password', type='password')

    if register_user_form.form_submit_button('Register'):
        if len(new_username) and len(new_name) and len(new_password) > 0:
            users = db.get_username(new_username)
            if users != None:
                st.error(f"❌ Ooops username dengan '{new_username}' sudah tersedia.")
                return False;
            if new_password == new_password_repeat:
                hashed_passwords = stauth.Hasher([new_password]).generate()[0]
                db.insert_user(new_username, new_name, hashed_passwords, "user")
                st.success(f"✔ Selamat anda sudah terdaftar {new_name}, **Silahkan login...**")
            else:
                st.warning("⚠ Oops.. password tidak valid")
        else:
            st.warning("⚠ Tolong masukan username, name and password")