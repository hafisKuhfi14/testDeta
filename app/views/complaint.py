import asyncio
import random
import streamlit as st  # pip install streamlit
from ..db import api

def complaint():
    st.markdown("### Input Keluhan Pelanggan")
    username = st.session_state['username']
    chatAsRole = "user"
    if (st.button("🔄 Refresh")):
        st.experimental_rerun()

    if (username == "admin"):
        chatAsRole = "assistant"
        users = asyncio.run(api.get_users())
        selected_tab = st.sidebar.selectbox("Select User", [item['username'] for item in users if item['username'] != 'admin'])
        messagesUser = []
        input_chat_disable = True
        if selected_tab is not None:
            found_user = next((item for item in users if item["username"] == selected_tab), None)
            messagesUser, messageChat = checkUser(found_user, selected_tab)
            print(messageChat)
            input_chat_disable = False

            if (st.button("Delete Chat")):
                if (len(messageChat) != 0):
                    asyncio.run(api.delete_chat({
                        "chat_id": messageChat['id'],
                        "username": selected_tab
                    }))
                asyncio.run(api.delete_user(found_user['id']))
                st.success("Delete user berhasil, harap refresh 🙏")
                st.experimental_rerun()
            # if found_user:
            #     st.write(f"Username: {found_user['username']}")
            #     st.write(f"Email: {found_user['email']}")
    else:
        users = asyncio.run(api.get_users())
        found_user = next((item for item in users if item["username"] == username), None)
        input_chat_disable = False
        if (found_user == None): 
            found_user = createUser(username)
        messagesUser, messageChat = checkUser(found_user, username)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    "---------"
    # Load session    
    st.session_state.messages = list(map(selectItem, messagesUser))
    for message in st.session_state.messages:
        if (message['role'] == 'user'):
            with st.chat_message("user"):
                st.markdown(f"##### :red[{message['sender_username']}]")
                st.markdown(message['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(message['content'])

    if (len(st.session_state.messages) == 0):
        with st.chat_message("assistant"):
            if (input_chat_disable) :
                st.markdown(f"Halo {username}👋, tidak ada keluhan saat ini")
            else:
                st.markdown(f"Halo {username}👋,\nApakah ada yang bisa saya bantu ?")

    "---------"
    # Chating with Users / Admin
    if prompt := st.chat_input("Whats is up ?", disabled=input_chat_disable):
        if (username != "admin" and len(messagesUser) <= 0):
            messageChat = createChat(username)
            ticket_complaint = f"Token keluhan anda: {messageChat['id']}, harap tunggu admin membalas dan refresh berkala 👋"
            st.session_state.messages.append({
                'role': 'assistant',
                'content': ticket_complaint
            })
            with st.chat_message("assistant"):
                st.markdown(ticket_complaint)
            
        with st.chat_message(chatAsRole):
            st.markdown(f"##### :red[{username}]")
            st.markdown(prompt)

            responseChat = asyncio.run(api.send_chat(prompt, {
                "chat_id": messageChat["id"],
                "username": username
            }))
            print(responseChat)
            st.session_state.messages.append({
                "role": "user",
                "content": responseChat["text"]
            })

def selectItem(x):
    # print(x)
    if (x['sender_username'] == "admin"):
        return {
            "sender_username": x['sender_username'],
            "role": "admin",
            "content": x['text']
        }
    else:
        return {
            "sender_username": x['sender_username'],
            "role": "user",
            "content": x['text']
        }
    
def checkUser(found_user, username):
    """
    checkUser apakah terdaftar ?\n
    jika belum maka daftarkan user tersebut, buat juga chat nya,\n
    jika sudah maka ambil chat yang sudah terdaftar (hanya 1)

    Returns
    ---\n
    > messageUser = all message \n
    > chats = your group chat
    """
    chats = asyncio.run(api.get_chats({
            "username": found_user['username']
    }))
    if (len(chats) <= 0):
        return [], chats
    chats = chats[0]
    chatUser = asyncio.run(api.get_message({
        "username": username,
        "chat_id": chats['id']
    }))
    
    return chatUser, chats

def createChat(username):
    chats = asyncio.run(api.new_chat("QNA", {
        "username": username
    }))
    responseAddAdmin = asyncio.run(api.add_chat_member("admin", {
        "username": username,
        "chat_id": chats['id']
    }))
    return chats

def createUser(username):
    response_create_user = asyncio.run(api.create_user({
        "username": username,
        "first_name": username,
        "last_name": username + f"{random.getrandbits(7)}",
        "secret": username,
        "custom_json": {
            "img": ""
        }
    }))

    return response_create_user