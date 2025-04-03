from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base User Model
class UserBase(BaseModel):
    username: str
    email: str
    # active: bool
    # admin: bool


# Schema for User Registration (Sign Up)
class UserCreate(UserBase):
    password: str  # Required for new user registration


# Schema for Updating User Info (Optional Password Update)
class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None
    admin: Optional[bool] = None
    password: Optional[str] = None 

# Schema for Returning User Details (Excluding Password)
class UserOut(UserBase):
    id: int
    last_login: Optional[datetime] = None 

    class Config:
      from_attributes = True 
# Enable SQLAlchemy ORM compatibility


# Schema for User Profile
class UserProfile(UserBase):
    id: int
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schema for Login Request (Separate from Registration)
class LoginRequest(BaseModel):
    email: str
    password: str


# Schema for JWT Token Response
class Token(BaseModel):
    access_token: str
    token_type: str


class SourceType:
    TEXT = "text"
    FILE = "file"
    Q_AND_A = "q_and_a"

class SourceContentStatus:
    INDEXED = "indexed"
    UNINDEXED = "unindexed"
    DELETED = "deleted"

class QueryRequest(BaseModel):
    user_id: int
    chat_id: int
    query: str

# ✅ Response Model
class QueryResponse(BaseModel):
    id: str
    content: str
    sender_role: str
    created_at: datetime
    answer: str    


# ChatMessage Model
class ChatMessageBase(BaseModel):
    sender: str  # "user" or "assistant"
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass  # No extra fields required when creating a message

class ChatMessageResponse(ChatMessageBase):
    id: int
    chat_id: int
    user_id: int
    sender: str  # <- This might not match your DB field name
    message: str  # <- This might not match your DB field name
    created_at: datetime
    class Config:
        from_attributes = True

# ChatSession Model
class ChatSessionBase(BaseModel):
    title: Optional[str] = None  # Title can be optional

class ChatSessionCreate(ChatSessionBase):
    user_id: int

class ChatSessionResponse(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

# ChatSummary Model
class ChatSummaryResponse(BaseModel):
    id: int
    chat_id: int
    summary_text: str
    last_updated: datetime

    class Config:
        from_attributes = True
