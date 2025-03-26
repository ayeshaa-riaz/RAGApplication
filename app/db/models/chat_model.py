from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.database import Base  # Assuming you have a database.py file with Base

# ✅ 2. Chat Sessions Table (Each session is a separate chat for a user)
# class ChatSession(Base):
#     __tablename__ = "chat_sessions"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     # Relationships
#     user = relationship("User", back_populates="chats")
#     messages = relationship("ChatMessage", back_populates="chat", cascade="all, delete-orphan")
#     summary = relationship("ChatSummary", uselist=False, back_populates="chat", cascade="all, delete-orphan")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String, nullable=True)  # Add this line

    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("ChatMessage", back_populates="chat", cascade="all, delete-orphan")
    summary = relationship("ChatSummary", uselist=False, back_populates="chat", cascade="all, delete-orphan")

# ✅ 3. Chat Messages Table (Stores individual messages)
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String, nullable=False)  # "user" or "assistant"
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chat = relationship("ChatSession", back_populates="messages")

# ✅ 4. Chat Summary Table (Stores summary for each chat)
class ChatSummary(Base):
    __tablename__ = "chat_summaries"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chat = relationship("ChatSession", back_populates="summary")
