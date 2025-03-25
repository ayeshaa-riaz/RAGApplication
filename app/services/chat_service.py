from sqlalchemy.orm import Session
from ..db.models.chat_model import ChatSession,ChatMessage
from ..db.schemas import schemas
from datetime import datetime

def save_chat_message(
    db: Session,
    user_id: int,
    content: str,
    response: str,
    collection_name: str
):
    # Create or get chat session
    chat = ChatSession(
        user_id=user_id,
        title=f"Chat with {collection_name}",
    )
    db.add(chat)
    db.flush()

    # Save user message
    user_message = ChatMessage(
        chat_id=chat.id,
        content=content,
        role="user"
    )
    db.add(user_message)

    # Save assistant response
    assistant_message = ChatMessage(
        chat_id=chat.id,
        content=response,
        role="assistant"
    )
    db.add(assistant_message)
    
    db.commit()
    return chat 