from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class TokenData(BaseModel):
    user_id: Optional[UUID] = None

