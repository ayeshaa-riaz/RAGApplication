from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import schemas
from app.services.auth_service import create_access_token, authenticate_user, create_user
from app.db.models.user_model import User

router = APIRouter(prefix="/auth", tags=["auth"])

# User Sign Up (Registration)
@router.post("/signup", response_model=schemas.UserProfile)
async def sign_up(
    user_create: schemas.UserCreate,  # Use UserCreate for registration
    db: Session = Depends(get_db)
):
    """Sign up a new user"""
    # Check if the user already exists

    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = create_user(db,user_create)
    return new_user  

# User Login (Authentication)
@router.post("/login", response_model=schemas.Token)
async def login(
    credentials: schemas.LoginRequest,  
    db: Session = Depends(get_db)
):
    """Log in an existing user and return a JWT token"""
    user = db.query(User).filter(User.email == credentials.email).first()
    authenticate_user(db,credentials)
   
    # Create and return an access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
