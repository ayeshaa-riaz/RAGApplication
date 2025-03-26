import streamlit as st
from app.ui.auth_ui import handle_login, handle_signup
from app.ui.chat_ui import display_chat
from app.ui.server_ui import check_server

def main():
    st.set_page_config(
        page_title="RAG Chatbot",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    for key in ["token", "chat_id", "messages", "server_status", "show_signup"]:
        if key not in st.session_state:
            st.session_state[key] = None if key in ["token", "chat_id"] else [] if key == "messages" else False

    # Check if FastAPI server is running
    if not check_server():
        st.error("""
            **FastAPI server is not running!**  
            Please start the backend with:  
            ```bash
            uvicorn app.main:app --reload
            ```
        """)
        return

    # Sidebar for authentication
    with st.sidebar:
        st.title("🔐 Authentication")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_btn"):
                st.session_state.show_signup = False
        with col2:
            if st.button("Sign Up", key="signup_btn"):
                st.session_state.show_signup = True

        if not st.session_state.show_signup:
            st.subheader("Login")
            handle_login()
        else:
            st.subheader("Sign Up")
            handle_signup()

    # Chat Interface
    st.title("🤖 RAG Chatbot")

    if st.session_state.token:
        display_chat()
    else:
        st.warning("Please log in to start chatting.")

if __name__ == "__main__":
    main()
