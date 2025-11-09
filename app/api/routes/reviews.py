from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.review import ReviewModifyModel
from app.services.review_service import add_review, edit_review, delete_review
from app.api.deps import get_current_user
from app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/api/movie", tags=["Reviews"])


@router.post("/{movieId}/review/add")
def add_movie_review(
    movieId: UUID,
    review_data: ReviewModifyModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a review to a movie."""
    add_review(db, current_user.id, movieId, review_data)
    return {"message": "Review added successfully"}


@router.put("/{movieId}/review/{id}/edit")
def edit_movie_review(
    movieId: UUID,
    id: UUID,
    review_data: ReviewModifyModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Edit a review."""
    edit_review(db, current_user.id, movieId, id, review_data)
    return {"message": "Review updated successfully"}


@router.delete("/{movieId}/review/{id}/delete")
def delete_movie_review(
    movieId: UUID,
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a review."""
    delete_review(db, current_user.id, movieId, id)
    return {"message": "Review deleted successfully"}

