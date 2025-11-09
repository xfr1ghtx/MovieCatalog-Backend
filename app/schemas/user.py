from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import IntEnum
from uuid import UUID


class Gender(IntEnum):
    Male = 0
    Female = 1


class UserShortModel(BaseModel):
    userId: UUID
    nickName: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileModel(BaseModel):
    id: UUID
    nickName: str
    email: EmailStr
    avatarLink: Optional[str] = None
    name: str
    birthDate: Optional[datetime] = None
    gender: Gender

    class Config:
        from_attributes = True

