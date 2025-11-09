from sqlalchemy.orm import Session
from app.models.favorite import FavoriteMovie
from app.models.movie import Movie
from app.schemas.movie import MoviesListModel, MovieElementModel, GenreModel
from app.schemas.review import ReviewModel
from app.schemas.user import UserShortModel
from app.core.exceptions import NotFoundException, ConflictException
from uuid import UUID


def get_favorite_movies(db: Session, user_id: UUID) -> MoviesListModel:
    """Get list of user's favorite movies."""
    favorites = db.query(FavoriteMovie).filter(FavoriteMovie.user_id == user_id).all()
    
    movie_elements = []
    for favorite in favorites:
        movie = db.query(Movie).filter(Movie.id == favorite.movie_id).first()
        if movie:
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
    
    return MoviesListModel(movies=movie_elements)


def add_favorite_movie(db: Session, user_id: UUID, movie_id: UUID) -> None:
    """Add movie to favorites."""
    # Check if movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise NotFoundException("Movie not found")
    
    # Check if already in favorites
    existing = db.query(FavoriteMovie).filter(
        FavoriteMovie.user_id == user_id,
        FavoriteMovie.movie_id == movie_id
    ).first()
    if existing:
        raise ConflictException("Movie already in favorites")
    
    # Add to favorites
    favorite = FavoriteMovie(user_id=user_id, movie_id=movie_id)
    db.add(favorite)
    db.commit()


def remove_favorite_movie(db: Session, user_id: UUID, movie_id: UUID) -> None:
    """Remove movie from favorites."""
    favorite = db.query(FavoriteMovie).filter(
        FavoriteMovie.user_id == user_id,
        FavoriteMovie.movie_id == movie_id
    ).first()
    if not favorite:
        raise NotFoundException("Movie not in favorites")
    
    db.delete(favorite)
    db.commit()

