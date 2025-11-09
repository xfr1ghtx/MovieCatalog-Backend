from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
from app.schemas.user import Gender


class UserRegisterModel(BaseModel):
    userName: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    email: EmailStr
    birthDate: Optional[datetime] = None
    gender: Gender
    
    @field_validator('birthDate')
    @classmethod
    def validate_birth_date(cls, v):
        if v:
            # Ensure both datetimes are timezone-aware for comparison
            now = datetime.now(timezone.utc)
            if v.tzinfo is None:
                # If v is naive, assume UTC
                v = v.replace(tzinfo=timezone.utc)
            if v > now:
                raise ValueError('Birth date cannot be in the future')
        return v


class LoginCredentials(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    token: str

