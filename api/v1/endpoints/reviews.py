from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from models.user import User
from models.review import Review
from schemas.review import ReviewRead, ReviewCreate, ReviewUpdate
import crud.review
import crud.image

router = APIRouter()

@router.post("/restaurant_id={restaurant_id}", response_model=ReviewRead)
def create_review(restaurant_id: int, review_create: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.review.create_review(db, current_user, restaurant_id, review_create)

@router.post("/{review_id}/images")
def upload_images(review_id: int, files: List[UploadFile] = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_review = crud.review.get_review(db, review_id)
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.image.upload_images(db, current_user, review_id, files)

@router.patch("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, review_update: ReviewUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_review = crud.review.get_review(db, review_id)
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.review.update_review(db, db_review, review_update)

@router.delete("/{review_id}")
def delete_review(review_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_review = crud.review.get_review(db, review_id)
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"detail": "Review deleted"}
    