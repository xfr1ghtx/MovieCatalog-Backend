from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.auth import UserRegisterModel, LoginCredentials, TokenResponse
from app.services.auth_service import register_user, login_user, logout_user
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/account", tags=["Account"])


@router.post("/register", response_model=TokenResponse)
def register(
    user_data: UserRegisterModel,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginCredentials,
    db: Session = Depends(get_db)
):
    """Login user."""
    return login_user(db, credentials)


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user."""
    logout_user(db, current_user.id, "")
    return {"message": "Successfully logged out"}

