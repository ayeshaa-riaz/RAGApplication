import streamlit as st
import requests
from typing import Optional

API_URL = "http://backend:8000"


def login(email: str, password: str) -> Optional[dict]:
    """Handle user login"""
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            data={"username": email, "password": password}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Login failed: {str(e)}")
        return None

def get_user_info(token: str) -> Optional[dict]:
    """Get user information from token"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/api/users/me",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get user info: {str(e)}")
        return None

def signup(username: str, email: str, password: str) -> Optional[dict]:
    """Handle user signup"""
    try:
        response = requests.post(
            f"{API_URL}/api/auth/signup",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Signup failed: {str(e)}")
        return None

def render_auth_page():
    """Render the authentication page"""
    st.title("Welcome to RAG Chat")
    
    # Toggle between login and signup
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="login_btn"):
            st.session_state.show_signup = False
    with col2:
        if st.button("Sign Up", key="signup_btn"):
            st.session_state.show_signup = True

    if not st.session_state.show_signup:
        # Login form
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_submit"):
            with st.spinner("Logging in..."):
                response = login(email, password)
                if response and "access_token" in response:
                    st.session_state.token = response["access_token"]
                    
                    # Get user info after successful login
                    user_info = get_user_info(response["access_token"])
                    if user_info:
                        st.session_state.user_id = user_info["id"]
                        st.success("Logged in successfully!")
                        st.rerun()
    else:
        # Signup form
        st.subheader("Sign Up")
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        if st.button("Sign Up", key="signup_submit"):
            if password != confirm_password:
                st.error("Passwords do not match!")
            else:
                with st.spinner("Creating account..."):
                    response = signup(username, email, password)
                    if response:
                        st.success("Account created successfully! Please login.")
                        st.session_state.show_signup = False
                        st.rerun()
