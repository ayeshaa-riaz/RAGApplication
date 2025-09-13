from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from services import chat_service, auth_service
from rag.chain import RAGChain
from db.schemas.schemas import ChatSessionCreate, QueryRequest, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from typing import List
from datetime import datetime
from db.models.chat_model import ChatSession, ChatMessage
import logging as logger


router = APIRouter()

# ✅ 1. Query Documents
@router.post("/query")
async def query_documents(
    query_request: QueryRequest,
    db: Session = Depends(get_db)
):
    query = query_request.query
    user_id = int(query_request.user_id)
    chat_id = int(query_request.chat_id)
    collection_name = "PrimaryCollection"
    
    try:
        logger.info(f"Processing query: {query}")
        chain = RAGChain(collection_name=collection_name)
        response = await chain.generate_response(question=query, user_id=user_id, chat_id=chat_id)
        
        return {
            "answer": response["answer"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in response["source_documents"]
            ],
            "chat_history": response["chat_history"]
        }
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

# ✅ 2. Start a New Chat
@router.post("/", response_model=ChatSessionResponse)
def create_chat(chat: ChatSessionCreate, db: Session = Depends(get_db)):
    new_chat = ChatSession(user_id=chat.user_id, title=chat.title)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

# ✅ 3. Get All Chats for a User
@router.get("/user/{user_id}", response_model=List[ChatSessionResponse])
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    chats = db.query(ChatSession).filter(ChatSession.user_id == user_id).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found for user")
    return chats

# ✅ 4. Delete a Chat
@router.delete("/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted"}

# ✅ 5. Send Messages (User and Assistant)
@router.post("/{chat_id}/messages/batch/", response_model=List[ChatMessageResponse])
def send_messages(chat_id: int, messages: List[ChatMessageCreate], db: Session = Depends(get_db)):
    """Handle both user and assistant messages in one request."""
    chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    saved_messages = []
    for message in messages:
        new_message = ChatMessage(
            chat_id=chat_id,
            user_id=chat.user_id,
            sender=message.sender,
            message=message.message
        )
        db.add(new_message)
        saved_messages.append(new_message)
    
    db.commit()
    for msg in saved_messages:
        db.refresh(msg)
    
    return saved_messages

# ✅ 6. Get All Messages in a Chat
@router.get("/{chat_id}/messages/", response_model=List[ChatMessageResponse])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    """Get all messages in a chat, ordered by message ID."""
    messages = db.query(ChatMessage).filter(
        ChatMessage.chat_id == chat_id
    ).order_by(ChatMessage.id.asc()).all()
    
    # Log message retrieval for debugging
    logger.info(f"Retrieved {len(messages)} messages for chat {chat_id}")
    if messages:
        logger.info(f"Message ID range: {messages[0].id} to {messages[-1].id}")
    
    return messages

