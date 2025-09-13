from sqlalchemy.orm import Session
from db.models.user_model import User
from db.schemas import schemas
from services.auth_service import get_password_hash
from fastapi import HTTPException, status

async def update_user_profile(
    db: Session, user_id: int, profile_update: schemas.UserProfileUpdate
):
    """Update the user's profile information in the database."""
    # Retrieve the user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update the fields that can be updated
    if profile_update.username:
        user.username = profile_update.username
    if profile_update.email:
        user.email = profile_update.email
    if profile_update.active is not None:
        user.active = profile_update.active
    if profile_update.admin is not None:
        user.admin = profile_update.admin

    # If a password is provided, hash and update it
    if profile_update.password:
        user.password = get_password_hash(profile_update.password)

    # Commit the changes to the database
    db.commit()
    db.refresh(user)

    return user
