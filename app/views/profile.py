import streamlit as st  # pip install streamlit
import pandas as pd
import app.db.database as db  # local import
import streamlit_authenticator as stauth

def profile():
    st.markdown("### User Management")
    if (st.session_state['username'] != "admin"):
        form_update(st.session_state['username'])
        return
    st.markdown("Data User")
    users = db.fetch_all_users()
    # Mengubah "key" menjadi "username"
    for item in users:
        item["username"] = item.pop("key")
        item.pop("password")

    st.dataframe(users ,use_container_width=True)
    updateUser, deleteUser = st.tabs(["Update", "Delete"])

    with updateUser:
        st.markdown("### Update")
        st.info("Silahkan pilih user ingin di update", icon="ℹ")
        st.write("Pilih username: ")
        selected_tab = st.selectbox("Select User", [user['username'] for user in users], key="update")
        if selected_tab is not None:
            form_update(selected_tab)
        
    with deleteUser:
        st.markdown("### Delete")
        st.info("Silahkan pilih user ingin di delete", icon="ℹ")
        selected_tab = st.selectbox("Select User", [user['username'] for user in users], key="delete")
        if selected_tab is not None:
            if (st.button("Delete") and st.session_state['username'] != selected_tab):
                user = db.delete_user(selected_tab)
                st.success(f"Success Delete {selected_tab}")
                st.experimental_rerun()
            if (selected_tab == st.session_state['username']):
                st.warning("Ooops tidak dapat menghapus diri sendiri")

def form_update(username):
    user = db.get_username(username)
    name = st.text_input("Nama: ", f"{user['name']}")
    password = st.text_input("Password: ", type='password')
    if (password != ""):
        password = stauth.Hasher([password]).generate()[0]
    else:
        password = user["password"]

    if (st.button("Update")):
        data = {
            "name":name, 
            "password":password
        }
        db.update_user(data, username)
        st.success(f"Success Update {name}")
        st.experimental_rerun()
