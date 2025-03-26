from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import schemas
from app.services.auth_service import get_current_user
from app.db.models.user_model import User
from app.services.user_service import update_user_profile

router = APIRouter()

# Get current user's profile
@router.get("/me", response_model=schemas.UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile"""
    return current_user

# Update current user's profile
@router.put("/me", response_model=schemas.UserProfile)
async def update_user_profile(
    profile_update: schemas.UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    return await update_user_profile(db, current_user.id, profile_update)
