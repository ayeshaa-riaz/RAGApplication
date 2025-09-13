from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from ..models import Base  # ✅ Use the same Base # Assuming you have a database.py file with Base

print("✅ user_model.py loaded")

# ✅ 1. Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chats = relationship("ChatSession", back_populates="user")