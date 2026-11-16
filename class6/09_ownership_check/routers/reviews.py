"""
Reviews router with an OWNERSHIP check:
  * anyone can read reviews
  * logged-in users can write reviews (owner_id = their id)
  * only the OWNER (or an admin) can edit/delete a review -> otherwise 403
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from database import DbSession
from models import Review, User
from schemas import ReviewCreate, ReviewOut, ReviewUpdate
from security import CurrentUser

router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_review_for_change(review_id: int, user: User, db) -> Review:
    """Load a review and make sure `user` may change it. Raises 404 or 403."""
    review = db.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    is_owner = review.owner_id == user.id
    if not (is_owner or user.role == "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only change your own reviews")
    return review


@router.get("", response_model=list[ReviewOut])
def list_reviews(db: DbSession):
    return db.scalars(select(Review).order_by(Review.id)).all()


@router.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(data: ReviewCreate, db: DbSession, user: CurrentUser):
    # owner_id comes from the TOKEN, never from the request body
    review = Review(**data.model_dump(), owner_id=user.id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.patch("/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, data: ReviewUpdate, db: DbSession, user: CurrentUser):
    review = get_review_for_change(review_id, user, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: DbSession, user: CurrentUser) -> None:
    review = get_review_for_change(review_id, user, db)
    db.delete(review)
    db.commit()
