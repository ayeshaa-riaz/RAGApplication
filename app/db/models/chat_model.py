from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.database import Base  


# ✅ 1. Chat Sessions Table (Stores chat metadata)
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String, nullable=False, default="New Chat")  # ✅ Default title

    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("ChatMessage", back_populates="chat", cascade="all, delete-orphan")
    summary = relationship("ChatSummary", uselist=False, back_populates="chat", cascade="all, delete-orphan")

# ✅ 2. Chat Messages Table (Stores individual messages)
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Add this line
    sender = Column(String, nullable=False)  # "user" or "assistant"
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chat = relationship("ChatSession", back_populates="messages")


# ✅ 3. Chat Summary Table (Stores summary for each chat)
class ChatSummary(Base):
    __tablename__ = "chat_summaries"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    summary_text = Column(Text, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Auto-update timestamp

    # Relationships
    chat = relationship("ChatSession", back_populates="summary")
