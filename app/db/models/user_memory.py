from sqlalchemy import Column, String, TIMESTAMP, ARRAY, text
from sqlalchemy.sql import func
from ..models import Base  # ✅ Use the same Base

class UserMemory(Base):
    __tablename__ = "user_memory"

    user_id = Column(String, primary_key=True)
    memory_context = Column(String)
    last_updated = Column(TIMESTAMP, server_default=func.now())
    topics = Column(ARRAY(String))
    books_engaged = Column(ARRAY(String))
    declined_questions = Column(ARRAY(String))
    tone_preference = Column(String) 


    