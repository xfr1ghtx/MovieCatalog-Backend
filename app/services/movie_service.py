from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.review import Review
from app.schemas.movie import (
    MovieElementModel,
    MovieDetailsModel,
    MoviesPagedListModel,
    PageInfoModel,
    GenreModel,
)
from app.schemas.review import ReviewModel
from app.schemas.user import UserShortModel
from app.core.exceptions import NotFoundException
from uuid import UUID
from typing import List


def get_movies_paged(db: Session, page: int = 1, page_size: int = 6) -> MoviesPagedListModel:
    """Get paginated list of movies."""
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get total count
    total_count = db.query(func.count(Movie.id)).scalar()
    
    # Calculate total pages
    total_pages = (total_count + page_size - 1) // page_size
    
    # Get movies
    movies = db.query(Movie).offset(offset).limit(page_size).all()
    
    # Convert to response model
    movie_elements = []
    for movie in movies:
        genres = [GenreModel(id=genre.id, name=genre.name) for genre in movie.genres]
        reviews = []
        for review in movie.reviews:
            author = None
            if not review.is_anonymous:
                author = UserShortModel(
                    userId=review.user.id,
                    nickName=review.user.username,
                    avatar=review.user.avatar_link,
                )
            reviews.append(
                ReviewModel(
                    id=review.id,
                    rating=review.rating,
                    reviewText=review.review_text,
                    isAnonymous=review.is_anonymous,
                    createDateTime=review.created_at,
                    author=author,
                )
            )
        
        movie_elements.append(
            MovieElementModel(
                id=movie.id,
                name=movie.name,
                poster=movie.poster,
                year=movie.year,
                country=movie.country,
                genres=genres,
                reviews=reviews,
            )
        )
    
    page_info = PageInfoModel(
        size=page_size,
        count=total_pages,
        current=page,
    )
    
    return MoviesPagedListModel(movies=movie_elements, pageInfo=page_info)


def get_movie_details(db: Session, movie_id: UUID) -> MovieDetailsModel:
    """Get detailed information about a movie."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise NotFoundException("Movie not found")
    
    # Convert genres
    genres = [GenreModel(id=genre.id, name=genre.name) for genre in movie.genres]
    
    # Convert reviews
    reviews = []
    for review in movie.reviews:
        author = None
        if not review.is_anonymous:
            author = UserShortModel(
                userId=review.user.id,
                nickName=review.user.username,
                avatar=review.user.avatar_link,
            )
        reviews.append(
            ReviewModel(
                id=review.id,
                rating=review.rating,
                reviewText=review.review_text,
                isAnonymous=review.is_anonymous,
                createDateTime=review.created_at,
                author=author,
            )
        )
    
    return MovieDetailsModel(
        id=movie.id,
        name=movie.name,
        poster=movie.poster,
        year=movie.year,
        country=movie.country,
        genres=genres,
        reviews=reviews,
        time=movie.time,
        tagline=movie.tagline,
        description=movie.description,
        director=movie.director,
        budget=movie.budget,
        fees=movie.fees,
        ageLimit=movie.age_limit,
    )

