import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta

# Load the environment variables
DETA_KEY = st.secrets["data_key"]
# DETA_KEY = "c0prthdezi3_8fUxGrrmpcp7cR8hNdag5NqVuzNh5UAd"

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("monthly_reports")

dbUser = deta.Base("users")


def fetch_all_users():
    """Returns a dict of all users"""
    res = dbUser.fetch()
    return res.items

def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return dbUser.put({"key": username, "name": name, "password": password})

def update_user(data, username):
    return dbUser.update(data, key=username)

def get_username(username):
    """If not found, the function will return None"""
    return dbUser.get(username)

def delete_user(username):
    return dbUser.delete(username)

def insert_complaint(name, complaint):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"name": name, "complaint": complaint})

def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)
