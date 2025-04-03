from sqlalchemy.orm import Session
from datetime import datetime
from langchain_community.chat_models import ChatCohere
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

from ..db.models.chat_model import ChatSession, ChatSummary, ChatMessage
from ..db.schemas import schemas



def create_chat(db: Session, chat_data: schemas.ChatSessionCreate) -> ChatSession:
    """
    Creates a new chat session for a user.
    
    Args:
        db (Session): The database session.
        chat_data (ChatSessionCreate): Pydantic schema with user_id and optional title.
    
    Returns:
        ChatSession: The created chat session object.
    """
    new_chat = ChatSession(user_id=chat_data.user_id, title=chat_data.title)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


def get_chat_by_id(db: Session, chat_id: int) -> ChatSession:
    """
    Retrieves a specific chat session by its ID.

    Args:
        db (Session): The database session.
        chat_id (int): The ID of the chat session.

    Returns:
        ChatSession: The chat session object if found, otherwise raises an exception.
    """
    chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not chat:
        raise ValueError("Chat not found")
    return chat


def get_chats_for_user(db: Session, user_id: int):
    """
    Fetches all chat sessions belonging to a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        List[ChatSession]: A list of the user's chat sessions.
    """
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).all()


def delete_chat(db: Session, chat_id: int) -> bool:
    """
    Deletes a chat session and its related messages and summary.

    Args:
        db (Session): The database session.
        chat_id (int): The ID of the chat session.

    Returns:
        bool: True if deletion was successful, False if chat was not found.
    """
    chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not chat:
        return False

    db.delete(chat)
    db.commit()
    return True


def create_message(db: Session, chat_id: int, message_data: schemas.ChatMessageCreate, user_id: int) -> ChatMessage:
    """
    Creates and saves a new message in a chat session.

    Args:
        db (Session): The database session.
        chat_id (int): The ID of the chat session.
        message_data (ChatMessageCreate): Pydantic schema with message details.
        user_id (int): The ID of the user sending the message.

    Returns:
        ChatMessage: The newly created message.
    """
    chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not chat:
        raise ValueError("Chat not found")

    new_message = ChatMessage(
        chat_id=chat_id,
        user_id=user_id,
        sender=message_data.sender,
        message=message_data.message,
        created_at=datetime.utcnow(),
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def get_messages_by_chat_id(db: Session, chat_id: int):
    """
    Retrieves all messages from a specific chat session.

    Args:
        db (Session): The database session.
        chat_id (int): The chat session ID.

    Returns:
        List[ChatMessage]: List of messages in the chat.
    """
    return db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).all()


async def get_chat_summary(db: Session, chat_id: int) -> str:
    """
    Retrieves the chat summary if available.

    Args:
        db (Session): The database session.
        chat_id (int): The chat session ID.

    Returns:
        str: The summary text or None if not found.
    """
    summary = db.query(ChatSummary).filter(ChatSummary.chat_id == chat_id).first()
    return summary.summary_text if summary else None


async def generate_summary(db: Session, chat_id: int):
    """
    Generates and stores a summary if chat messages exceed a memory limit.

    Args:
        db (Session): The database session.
        chat_id (int): The chat session ID.

    Returns:
        None: Updates the database with the new summary.
    """
    messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).all()

    if not messages:
        return

    chat_text = "\n".join([f"{msg.sender}: {msg.message}" for msg in messages])
    docs = [Document(page_content=chat_text)]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"), model="command", temperature=0)
    chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
    summary = chain.run(split_docs)

    existing_summary = db.query(ChatSummary).filter(ChatSummary.chat_id == chat_id).first()
    if existing_summary:
        existing_summary.summary_text = summary
        existing_summary.last_updated = datetime.utcnow()
    else:
        db.add(ChatSummary(chat_id=chat_id, summary_text=summary, last_updated=datetime.utcnow()))

    db.commit()
