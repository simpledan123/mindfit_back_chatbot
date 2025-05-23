from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from models.restaurant import Restaurant

def get_user_bookmarks(db: Session, user: User):
    return user.bookmarked_restaurants

def create_bookmark(db: Session, user: User, restaurant_id: int):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if restaurant in user.bookmarked_restaurants:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    
    user.bookmarked_restaurants.append(restaurant)
    db.commit()
    return restaurant

def delete_bookmark(db: Session, user: User, restaurant_id: int):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if restaurant in user.bookmarked_restaurants:
        user.bookmarked_restaurants.remove(restaurant)
        db.commit()
