from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user import ProfileModel
from app.services.user_service import get_user_profile, update_user_profile
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/account", tags=["Account"])


@router.get("/profile", response_model=ProfileModel)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile."""
    return get_user_profile(db, current_user.id)


@router.put("/profile", response_model=ProfileModel)
def update_profile(
    profile_data: ProfileModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile."""
    return update_user_profile(db, current_user.id, profile_data)

