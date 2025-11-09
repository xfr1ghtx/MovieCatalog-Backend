from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.schemas.user import UserShortModel


class ReviewModifyModel(BaseModel):
    reviewText: str = Field(..., min_length=1)
    rating: int = Field(..., ge=0, le=10)
    isAnonymous: bool = False


class ReviewShortModel(BaseModel):
    id: UUID
    rating: int

    class Config:
        from_attributes = True


class ReviewModel(BaseModel):
    id: UUID
    rating: int
    reviewText: str
    isAnonymous: bool
    createDateTime: datetime
    author: Optional[UserShortModel] = None

    class Config:
        from_attributes = True

