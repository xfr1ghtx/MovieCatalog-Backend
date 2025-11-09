from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.movie import MoviesListModel
from app.services.favorite_service import get_favorite_movies, add_favorite_movie, remove_favorite_movie
from app.api.deps import get_current_user
from app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/api/favorites", tags=["Favorites"])


@router.get("/", response_model=MoviesListModel)
def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's favorite movies."""
    return get_favorite_movies(db, current_user.id)


@router.post("/{id}/add")
def add_to_favorites(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add movie to favorites."""
    add_favorite_movie(db, current_user.id, id)
    return {"message": "Movie added to favorites"}


@router.delete("/{id}/delete")
def remove_from_favorites(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove movie from favorites."""
    remove_favorite_movie(db, current_user.id, id)
    return {"message": "Movie removed from favorites"}

