import streamlit as st
import requests
from datetime import datetime
from typing import List, Dict, Optional
from server_ui import get_chat_history
import json
import logging

API_URL = "http://backend:8000"

logger = logging.getLogger(__name__)

def start_chat(token: str) -> Optional[dict]:
    """Start a new chat session"""
    try:
        # Get user_id if not in session state
        if "user_id" not in st.session_state:
            headers = {"Authorization": f"Bearer {token}"}
            user_response = requests.get(
                f"{API_URL}/api/users/me",
                headers=headers
            )
            user_response.raise_for_status()
            user_data = user_response.json()
            st.session_state.user_id = user_data["id"]

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/api/chat/",
            headers=headers,
            json={
                "user_id": st.session_state.user_id,
                "title": f"New Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to start chat: {str(e)}")
        return None

def get_user_chats(token: str) -> List[Dict]:
    """Get all chats for the current user"""
    try:
        # First get user info from token
        headers = {"Authorization": f"Bearer {token}"}
        user_response = requests.get(
            f"{API_URL}/api/users/me",
            headers=headers
        )
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Store user_id in session state
        st.session_state.user_id = user_data["id"]
        
        # Now get user's chats
        response = requests.get(
            f"{API_URL}/api/chat/user/{user_data['id']}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get chats: {str(e)}")
        return []

def send_messages(chat_id: int, messages: List[dict], token: str) -> Optional[List[dict]]:
    """Send multiple messages to the chat"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # Format messages according to the API's expected schema
        formatted_messages = [
            {
                "sender": msg["sender"],
                "message": msg["message"]
            }
            for msg in messages
        ]
        logger.info(f"Sending messages to chat {chat_id}: {formatted_messages}")
        response = requests.post(
            f"{API_URL}/api/chat/{chat_id}/messages/batch/",
            headers=headers,
            json=formatted_messages
        )
        response.raise_for_status()
        saved_messages = response.json()
        logger.info(f"Successfully saved messages: {saved_messages}")
        return saved_messages
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send messages: {str(e)}", exc_info=True)
        st.error(f"Failed to send messages: {str(e)}")
        return None

def get_chat_messages(chat_id: int, token: str) -> List[Dict]:
    """Get chat messages ordered by message ID"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/api/chat/{chat_id}/messages/",
            headers=headers
        )
        response.raise_for_status()
        messages = response.json()
        
        # Sort messages by ID to ensure correct order
        messages.sort(key=lambda x: x.get('id', 0))
        
        # Log message IDs for debugging
        logger.info(f"Retrieved {len(messages)} messages")
        if messages:
            logger.info(f"Message ID range: {messages[0].get('id')} to {messages[-1].get('id')}")
            
        return messages
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get messages: {str(e)}")
        st.error(f"Failed to get messages: {str(e)}")
        return []

def render_chat_page():
    """Render the chat interface."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_id" not in st.session_state:
        st.error("Please login first")
        return

    # Sidebar for chat selection
    with st.sidebar:
        st.subheader("Your Chats")
        
        # Get all chats for the user
        chats = get_user_chats(st.session_state.token)
        
        # Button to create new chat
        if st.button("New Chat"):
            chat_response = start_chat(st.session_state.token)
            if chat_response:
                st.session_state.chat_id = chat_response["id"]
                st.session_state.messages = []  # Clear messages for new chat
                st.rerun()
        
        # Display existing chats with 3-dot menu
        for chat in chats:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(chat["title"], key=f"chat_{chat['id']}"):
                    st.session_state.chat_id = chat["id"]
                    st.session_state.messages = get_chat_messages(chat["id"], st.session_state.token)
                    st.rerun()
            
            with col2:
                if st.button("⋮", key=f"menu_{chat['id']}"):
                    st.session_state.selected_chat = chat["id"]
            
            # Show delete option if chat is selected
            if hasattr(st.session_state, 'selected_chat') and st.session_state.selected_chat == chat["id"]:
                if st.button("Delete Chat", key=f"delete_{chat['id']}"):
                    try:
                        response = requests.delete(
                            f"{API_URL}/api/chat/{chat['id']}",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        if response.status_code == 200:
                            st.success("Chat deleted successfully")
                            if st.session_state.chat_id == chat["id"]:
                                st.session_state.chat_id = None
                                st.session_state.messages = []
                            st.rerun()
                        else:
                            st.error("Failed to delete chat")
                    except Exception as e:
                        st.error(f"Error deleting chat: {str(e)}")

    # Main chat area
    if "chat_id" not in st.session_state or not st.session_state.chat_id:
        st.info("Select a chat from the sidebar or create a new one!")
        return

    # Display chat messages
    messages = sorted(st.session_state.messages, key=lambda x: x.get('id', 0))
    for message in messages:
        with st.chat_message(message["sender"]):
            st.markdown(message["message"])
            logger.info(f"Displaying message ID: {message.get('id')}")
            if "source_documents" in message:
                with st.expander("View Sources"):
                    for doc in message["source_documents"]:
                        st.markdown(f"**Content:** {doc['content'][:200]}...")
                        st.markdown(f"**Source:** {doc['metadata'].get('source', 'Unknown')}")
                        st.divider()

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({
            "sender": "user",
            "message": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)


        # Show assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Call the RAG endpoint
                    response = requests.post(
                        f"{API_URL}/api/chat/query",
                        json={
                            "query": prompt,
                            "user_id": st.session_state.user_id,
                            "chat_id": st.session_state.chat_id,
                            "collection_name": "PrimaryCollection"
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        
                        # Add assistant message to chat history
                        st.session_state.messages.append({
                            "sender": "assistant",
                            "message": result["answer"],
                            "source_documents": result["source_documents"]
                        })
                        
                        # Display the response
                        st.markdown(result["answer"])
                        
                        # Show source documents in an expander
                        with st.expander("View Sources"):
                            for doc in result["source_documents"]:
                                st.markdown(f"**Content:** {doc['content'][:200]}...")
                                st.markdown(f"**Source:** {doc['metadata'].get('source', 'Unknown')}")
                                st.divider()
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    logger.error(f"Error in chat: {str(e)}", exc_info=True)
                    st.error("An error occurred while processing your request.")


