from sqlalchemy.orm import Session
from app.models.user import User
from app.models.token import RefreshToken
from app.schemas.auth import UserRegisterModel, LoginCredentials
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    get_token_expire_time,
)
from app.core.exceptions import ConflictException, UnauthorizedException
from uuid import UUID


def register_user(db: Session, user_data: UserRegisterModel) -> dict:
    """Register a new user."""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.userName).first()
    if existing_user:
        raise ConflictException("Username already registered")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise ConflictException("Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.userName,
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password,
        birth_date=user_data.birthDate,
        gender=user_data.gender,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})
    
    # Save refresh token to database
    refresh_token_obj = RefreshToken(
        user_id=new_user.id,
        token=refresh_token,
        expires_at=get_token_expire_time("refresh"),
    )
    db.add(refresh_token_obj)
    db.commit()
    
    return {"token": access_token}


def login_user(db: Session, credentials: LoginCredentials) -> dict:
    """Authenticate user and return access token."""
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise UnauthorizedException("Invalid credentials")
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise UnauthorizedException("Invalid credentials")
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Save refresh token to database
    refresh_token_obj = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=get_token_expire_time("refresh"),
    )
    db.add(refresh_token_obj)
    db.commit()
    
    return {"token": access_token}


def logout_user(db: Session, user_id: UUID, token: str) -> None:
    """Logout user by removing refresh token."""
    # Remove all refresh tokens for this user (logout from all devices)
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()

