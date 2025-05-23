from sqlalchemy.orm import Session
from models.user import User
from models.review import Review
from schemas.review import ReviewCreate, ReviewUpdate\

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def create_review(db: Session, user: User, restaurant_id: int, review_create: ReviewCreate):
    db_review = Review(
        rating=review_create.rating,
        comment=review_create.comment,
        user_id=user.id,
        restaurant_id=restaurant_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, db_review: Review, review_update: ReviewUpdate):
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = get_review(db, review_id)
    db.delete(db_review)
    db.commit()