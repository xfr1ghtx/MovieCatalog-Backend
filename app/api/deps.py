from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.core.security import decode_token
from app.models.user import User
from app.core.exceptions import UnauthorizedException
from uuid import UUID

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise UnauthorizedException("Could not validate credentials")
    
    # Get user_id from token
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise UnauthorizedException("Could not validate credentials")
    
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException("Could not validate credentials")
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("User not found")
    
    return user

