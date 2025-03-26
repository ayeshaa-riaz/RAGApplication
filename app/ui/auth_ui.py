import streamlit as st
from ui.server_ui import login, signup, start_chat

def handle_login():
    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔑 Password", type="password", key="login_password")
    
    if st.button("Login", key="login_submit"):
        with st.spinner("Logging in..."):
            response = login(email, password)
            if response and "access_token" in response:
                st.session_state.token = response["access_token"]
                st.success("✅ Logged in successfully!")
                
                chat_response = start_chat(st.session_state.token)
                if chat_response and "id" in chat_response:
                    st.session_state.chat_id = chat_response["id"]
                    st.success("💬 New chat started!")
            else:
                st.error(response.get("error", "❌ Login failed!"))

def handle_signup():
    username = st.text_input("👤 Username", key="signup_username")
    email = st.text_input("📧 Email", key="signup_email")
    password = st.text_input("🔑 Password", type="password", key="signup_password")
    confirm_password = st.text_input("🔒 Confirm Password", type="password", key="signup_confirm_password")
    
    if st.button("Sign Up", key="signup_submit"):
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            with st.spinner("Creating account..."):
                response = signup(email, password, username)
                if response:
                    st.success("✅ Account created! Please log in.")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error("❌ Signup failed")
