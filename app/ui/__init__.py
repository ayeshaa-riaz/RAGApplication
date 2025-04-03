import streamlit as st
from app.ui.auth_ui import render_auth_page
from app.ui.chat_ui import render_chat_page
from app.ui.server_ui import render_server_status

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

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="RAG Chat Application",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    
    # Check server status first
    render_server_status()
    
    # Show appropriate page based on authentication
    if st.session_state.token:
        render_chat_page()
    else:
        render_auth_page()

if __name__ == "__main__":
    main()
