from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from models.user import User
from schemas.bookmark import BookmarkCreate, BookmarkRead
import crud.bookmark

router = APIRouter()

@router.get("/", response_model=List[BookmarkRead])
def read_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookmarks = crud.bookmark.get_user_bookmarks(db, current_user)
    return bookmarks

@router.post("/restaurant_id={restaurant_id}", response_model=BookmarkRead)
def create_bookmark(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookmarked_restaurant = crud.bookmark.create_bookmark(db, current_user, restaurant_id)
    return bookmarked_restaurant

@router.delete("/restaurant_id={restaurant_id}", status_code=204)
def delete_bookmark(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud.bookmark.delete_bookmark(db, current_user, restaurant_id)
    return
