import streamlit as st
import requests
from auth_ui import render_auth_page
from chat_ui import render_chat_page
from server_ui import render_server_status

# API_URL = "http://ragapplication-backend-1:8000"
 # Confirm this is correct for your environment
API_URL = "http://backend:8000"

def init_session_state():
    """Initialize session state variables"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = None
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

def check_backend():
    """Check if FastAPI backend is reachable"""
    try:
        # You can ping the /docs or create a /health endpoint on FastAPI for this purpose
        response = requests.get(f"{API_URL}/docs", timeout=3)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Backend returned unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot reach backend server: {e}")
        return False

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="RAG Chat Application",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    
    # Backend health check
    if not check_backend():
        st.stop()  # Stop the app here if backend is down
    
    # Check server status UI (optional, or you can remove if redundant)
    render_server_status()
    
    # Show appropriate page based on authentication
    if st.session_state.token:
        render_chat_page()
    else:
        render_auth_page()

if __name__ == "__main__":
    main()
