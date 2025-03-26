from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import schemas
from app.services import auth_service
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter()

# User Sign Up (Registration)
@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    """
    # Check if user already exists
    db_user = auth_service.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    return auth_service.create_user(db=db, user=user)

# User Login (Authentication)
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token.
    """
    user = auth_service.authenticate_user(db, form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
