import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    poster = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    time = Column(Integer, nullable=False)  # Продолжительность в минутах
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    director = Column(String, nullable=True)
    budget = Column(Integer, nullable=True)
    fees = Column(Integer, nullable=True)
    age_limit = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    genres = relationship("Genre", secondary="movie_genres", backref="movies")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")


class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(UUID(as_uuid=True), ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)

