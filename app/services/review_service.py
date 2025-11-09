from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.movie import Movie
from app.schemas.review import ReviewModifyModel
from app.core.exceptions import NotFoundException, ConflictException, ForbiddenException
from uuid import UUID


def add_review(db: Session, user_id: UUID, movie_id: UUID, review_data: ReviewModifyModel) -> None:
    """Add a review to a movie."""
    # Check if movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise NotFoundException("Movie not found")
    
    # Check if user already reviewed this movie
    existing_review = db.query(Review).filter(
        Review.user_id == user_id,
        Review.movie_id == movie_id
    ).first()
    if existing_review:
        raise ConflictException("You have already reviewed this movie")
    
    # Create review
    review = Review(
        movie_id=movie_id,
        user_id=user_id,
        rating=review_data.rating,
        review_text=review_data.reviewText,
        is_anonymous=review_data.isAnonymous,
    )
    db.add(review)
    db.commit()


def edit_review(
    db: Session,
    user_id: UUID,
    movie_id: UUID,
    review_id: UUID,
    review_data: ReviewModifyModel
) -> None:
    """Edit a review."""
    # Get review
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise NotFoundException("Review not found")
    
    # Check if review belongs to the movie
    if review.movie_id != movie_id:
        raise NotFoundException("Review not found for this movie")
    
    # Check if user is the author
    if review.user_id != user_id:
        raise ForbiddenException("You can only edit your own reviews")
    
    # Update review
    review.rating = review_data.rating
    review.review_text = review_data.reviewText
    review.is_anonymous = review_data.isAnonymous
    
    db.commit()


def delete_review(db: Session, user_id: UUID, movie_id: UUID, review_id: UUID) -> None:
    """Delete a review."""
    # Get review
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise NotFoundException("Review not found")
    
    # Check if review belongs to the movie
    if review.movie_id != movie_id:
        raise NotFoundException("Review not found for this movie")
    
    # Check if user is the author
    if review.user_id != user_id:
        raise ForbiddenException("You can only delete your own reviews")
    
    db.delete(review)
    db.commit()

