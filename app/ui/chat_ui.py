import streamlit as st
from ui.server_ui import send_message, get_chat_messages

import streamlit as st
import requests
from ui.server_ui import send_message, get_chat_messages, get_chat_history, start_chat

API_URL = "http://localhost:8000"  # Update with your API URL

def chat_sidebar():
    """Sidebar for chat history and starting new chats"""
    with st.sidebar:
        st.title("💬 Chat History")
        
        if "token" not in st.session_state or not st.session_state.token:
            st.warning("⚠️ Please log in to view chats.")
            return
        
        chats = get_chat_history(st.session_state.token)
        if "error" in chats:
            st.error(chats["error"])
            return
        
        chat_titles = {chat["id"]: chat["title"] for chat in chats}
        
        if chat_titles:
            selected_chat = st.radio("📜 Select a chat:", options=chat_titles.keys(), format_func=lambda x: chat_titles[x])
            if st.button("Load Chat"):
                st.session_state.chat_id = selected_chat
                st.session_state.messages = get_chat_messages(selected_chat, st.session_state.token)
                st.rerun()

        if st.button("➕ Start New Chat"):
            new_chat = start_chat(st.session_state.token)
            if "error" in new_chat:
                st.error(new_chat["error"])
            else:
                st.session_state.chat_id = new_chat["id"]
                st.session_state.messages = []
                st.success("✅ New chat started!")
                st.rerun()

def display_chat():
    """Main chat interface"""
    if not st.session_state.get("token"):
        st.warning("⚠️ You need to log in to start chatting.")
        return
    
    chat_sidebar()  # Show chat history in sidebar
    
    if not st.session_state.get("chat_id"):
        st.warning("⚠️ No active chat found. Please start a new chat.")
        return
    
    messages = st.session_state.get("messages", [])
    
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("💬 Ask me something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.spinner("Thinking... 🤔"):
            response = send_message(st.session_state.chat_id, prompt, st.session_state.token)
            if response and "content" in response:
                ai_message = response["content"]
                st.session_state.messages.append({"role": "assistant", "content": ai_message})
                with st.chat_message("assistant"):
                    st.write(ai_message)
                    
                    if "source_documents" in response:
                        with st.expander("📖 View Sources"):
                            for doc in response["source_documents"]:
                                st.text(doc["page_content"])
