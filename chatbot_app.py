import streamlit as st
import sqlite3
from transformers import pipeline
from datetime import datetime

# Initialize the chatbot using Hugging Face Transformers (DistilBERT model)
chatbot = pipeline('conversational', model='microsoft/DialoGPT-medium')

# Connect to SQLite database for user authentication
def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY, 
                        username TEXT UNIQUE, 
                        password TEXT, 
                        email TEXT)''')
    conn.commit()
    conn.close()

def register_user(username, password, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username, password, email) 
                      VALUES (?, ?, ?)''', (username, password, email))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_profile(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username=?''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# User authentication page
def login_page():
    st.title('Login to Chatbot')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        user = authenticate_user(username, password)
        if user:
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
            chatbot_page()
        else:
            st.error('Invalid credentials')

def register_page():
    st.title('Register for Chatbot')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    email = st.text_input('Email')
    
    if st.button('Register'):
        try:
            register_user(username, password, email)
            st.success("Registration Successful! Please login.")
        except sqlite3.IntegrityError:
            st.error("Username already exists!")

# Chatbot interface
def chatbot_page():
    st.title('Chatbot Interface')
    
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if 'username' in st.session_state:
        user_profile = get_user_profile(st.session_state.username)
        st.write(f"User Profile - Username: {user_profile[1]}, Email: {user_profile[3]}")
    
    user_input = st.text_input("Say something to the bot:")
    if user_input:
        response = chatbot(user_input)[0]['generated_text']
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Bot: {response}")
    
    if st.session_state.history:
        st.write("\n".join(st.session_state.history))

# Main logic to control flow
def main():
    st.set_page_config(page_title="Chatbot App", layout="wide")
    create_db()
    
    if 'username' not in st.session_state:
        choice = st.selectbox('Choose an option', ['Login', 'Register'])
        
        if choice == 'Login':
            login_page()
        elif choice == 'Register':
            register_page()
    else:
        chatbot_page()

if __name__ == '__main__':
    main()
