from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import ProfileModel
from app.core.exceptions import NotFoundException
from uuid import UUID


def get_user_profile(db: Session, user_id: UUID) -> ProfileModel:
    """Get user profile."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")
    
    return ProfileModel(
        id=user.id,
        nickName=user.username,
        email=user.email,
        avatarLink=user.avatar_link,
        name=user.name,
        birthDate=user.birth_date,
        gender=user.gender,
    )


def update_user_profile(db: Session, user_id: UUID, profile_data: ProfileModel) -> ProfileModel:
    """Update user profile."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")
    
    # Update fields
    user.email = profile_data.email
    user.avatar_link = profile_data.avatarLink
    user.name = profile_data.name
    user.birth_date = profile_data.birthDate
    user.gender = profile_data.gender
    
    db.commit()
    db.refresh(user)
    
    return ProfileModel(
        id=user.id,
        nickName=user.username,
        email=user.email,
        avatarLink=user.avatar_link,
        name=user.name,
        birthDate=user.birth_date,
        gender=user.gender,
    )

