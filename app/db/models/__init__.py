# app/db/models/__init__.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # ✅ This is the ONE Base used everywhere

from .user_model import User
from .chat_model import ChatSession, ChatMessage
from .user_memory import UserMemory

__all__ = ["Base", "User", "ChatSession", "ChatMessage", "UserMemory"]
