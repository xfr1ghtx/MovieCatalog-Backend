from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.schemas.review import ReviewModel


class GenreModel(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class MovieElementModel(BaseModel):
    id: UUID
    name: str
    poster: str
    year: int
    country: str
    genres: List[GenreModel]
    reviews: List["ReviewModel"]

    class Config:
        from_attributes = True


class MovieDetailsModel(BaseModel):
    id: UUID
    name: str
    poster: str
    year: int
    country: str
    genres: List[GenreModel]
    reviews: List["ReviewModel"]
    time: int
    tagline: Optional[str] = None
    description: Optional[str] = None
    director: Optional[str] = None
    budget: Optional[int] = None
    fees: Optional[int] = None
    ageLimit: int

    class Config:
        from_attributes = True


class MoviesListModel(BaseModel):
    movies: List[MovieElementModel]


class PageInfoModel(BaseModel):
    size: int
    count: int
    current: int


class MoviesPagedListModel(BaseModel):
    movies: List[MovieElementModel]
    pageInfo: PageInfoModel

