import requests
import streamlit as st
from typing import Optional

API_URL = "http://localhost:8000"

def check_server() -> bool:
    """Check if the FastAPI server is running"""
    try:
        requests.get(f"{API_URL}/docs")
        return True
    except requests.exceptions.ConnectionError:
        return False

def render_server_status():
    """Render server status page"""
    st.title("Server Status")
    
    if check_server():
        st.success("FastAPI server is running!")
    else:
        st.error("""
            FastAPI server is not running. Please start the server first:
            ```bash
            uvicorn app.main:app --reload
            ```
        """)

def login(email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json={"email": email, "password": password}
            
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Login failed: {str(e)}"}

def signup(email: str, password: str, username: str):
    try:
        response = requests.post(
            f"{API_URL}/api/auth/signup",
            json={"email": email, "password": password, "username": username}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Signup failed: {str(e)}"}

def start_chat(token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/api/chat/start-chat",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Failed to start chat: {str(e)}"}

def get_chat_messages(chat_id: int, token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/chat/{chat_id}/messages", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Failed to fetch messages: {str(e)}"}

def send_message(chat_id: int, message: str, token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/api/chat/{chat_id}/message",
            headers=headers,
            json={"content": message, "role": "user"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Failed to send message: {str(e)}"}

def get_chat_history(token: str):
    """Fetch all chats for the user."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/chat/history", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Failed to fetch chat history: {str(e)}"}
