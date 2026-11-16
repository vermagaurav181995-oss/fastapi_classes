"""Reviews: public reads, users write, only the OWNER or an admin may edit/delete."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from database import DbSession
from exceptions import NotFoundError
from models import Book, Review, User
from schemas import ReviewCreate, ReviewOut, ReviewUpdate
from security import CurrentUser

router = APIRouter(tags=["reviews"])


def get_review_for_change(review_id: int, user: User, db) -> Review:
    review = db.get(Review, review_id)
    if review is None:
        raise NotFoundError("Review", review_id)
    if review.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only change your own reviews")
    return review


@router.get("/books/{book_id}/reviews", response_model=list[ReviewOut])
def list_reviews(book_id: int, db: DbSession):
    if db.get(Book, book_id) is None:
        raise NotFoundError("Book", book_id)
    return db.scalars(select(Review).where(Review.book_id == book_id).order_by(Review.id)).all()


@router.post("/books/{book_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(book_id: int, data: ReviewCreate, db: DbSession, user: CurrentUser):
    if db.get(Book, book_id) is None:
        raise NotFoundError("Book", book_id)
    review = Review(**data.model_dump(), book_id=book_id, owner_id=user.id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.patch("/reviews/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, data: ReviewUpdate, db: DbSession, user: CurrentUser):
    review = get_review_for_change(review_id, user, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: DbSession, user: CurrentUser) -> None:
    db.delete(get_review_for_change(review_id, user, db))
    db.commit()
