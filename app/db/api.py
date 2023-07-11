import streamlit as st  # pip install streamlit

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ID = st.secrets["Project_ID"]
PRIVATE_KEY = st.secrets["Private_KEY"]

class User(BaseModel):
    username: str

async def authenticate(user:User):
    response = requests.put('https://api.chatengine.io/users/',
        data={
            "username": user.username,
            "secret": user.username,
            "first_name": user.username,
        },
        headers={ "Project-ID": PROJECT_ID, "Private-Key": PRIVATE_KEY }
    )
    return response.json()

async def send_chat(txt, credential):
    response = requests.post(f"https://api.chatengine.io/chats/{credential['chat_id']}/messages/",
        headers={
            "Project-ID": PROJECT_ID,
            "User-Name": credential['username'],
            "User-Secret": credential['username']
        }, data={
            "text": txt
        })
    return response.json()

async def new_chat(title, credential):
    response = requests.post(f"https://api.chatengine.io/chats/",
        headers={
            "Project-ID": PROJECT_ID,
            "Private-Key": PRIVATE_KEY,
            "User-Name": credential['username'],
            "User-Secret": credential['username']
        }, data= {
            "title": title,
            "is_direct_chat": False
        })
    return response.json()

async def get_chats(credential):
    response = requests.get(f"https://api.chatengine.io/chats/",
        headers={
            "Project-ID": PROJECT_ID,
            "Private-Key": PRIVATE_KEY,
            "User-Name": credential['username'],
            "User-Secret": credential['username']
        })
    return response.json()

async def delete_chat(credential):
    response = requests.delete(f"https://api.chatengine.io/chats/{credential['chat_id']}/",
            headers={
                "Project-ID": PROJECT_ID,
                "User-Name": credential['username'],
                "User-Secret": credential['username']
            })
    
    return response.json()

async def get_message(credential):
    response = requests.get(f"https://api.chatengine.io/chats/{credential['chat_id']}/messages/",
        headers={
            "Project-ID": PROJECT_ID,
            "Private-Key": PRIVATE_KEY,
            "User-Name": credential['username'],
            "User-Secret": credential['username']
        })
    return response.json()

async def add_chat_member(admin, credential):
    response = requests.post(f"https://api.chatengine.io/chats/{credential['chat_id']}/people/",
        headers={
            "Project-ID": PROJECT_ID,
            "User-Name": credential['username'],
            "User-Secret": credential['username']
        }, data= {
            "username": admin
        })
    return response.json()

async def create_user(body):
    response = requests.post(f"https://api.chatengine.io/users/",
        headers={
            "Private-Key": PRIVATE_KEY
        }, data= body)
    return response.json()

async def get_users():
    response = requests.get(f"https://api.chatengine.io/users/",
        headers={
            "Private-Key": PRIVATE_KEY
        })
    return response.json()

async def get_user_detail(id):
    response = requests.get(f"https://api.chatengine.io/users/{id}/",
        headers={
            "Private-Key": PRIVATE_KEY
        })
    return response.json()

async def delete_user(user_id):
    response = requests.delete(f"https://api.chatengine.io/users/{user_id}/", 
        headers={
            "Private-Key": PRIVATE_KEY
        })
    return response.json()

async def get_user_by_username(username, users):
    found_data = None
    for item in users:
        if item["username"] == username:
            found_data = item
            break
    return found_data