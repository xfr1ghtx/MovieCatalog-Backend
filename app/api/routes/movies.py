from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.movie import MovieDetailsModel, MoviesPagedListModel
from app.services.movie_service import get_movies_paged, get_movie_details
from uuid import UUID

router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.get("/{page}", response_model=MoviesPagedListModel)
def get_movies(
    page: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Get paginated list of movies."""
    return get_movies_paged(db, page)


@router.get("/details/{id}", response_model=MovieDetailsModel)
def get_movie(
    id: UUID,
    db: Session = Depends(get_db)
):
    """Get movie details."""
    return get_movie_details(db, id)

