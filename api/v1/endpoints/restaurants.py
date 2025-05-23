from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_admin_user
from models.user import User
from schemas.restaurant import RestaurantRead, RestaurantReadWithReviews, RestaurantCreate, RestaurantUpdate
import crud.restaurant

router = APIRouter()

@router.get("/{restaurant_id}", response_model=RestaurantReadWithReviews, response_model_exclude={"reviews": {"__all__": {"images"}}})
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    current_restaurant = crud.restaurant.get_restaurant(db, restaurant_id)
    return current_restaurant

@router.post("/", response_model=RestaurantRead)
def create_restaurant(restaurant_create: RestaurantCreate,
                    db: Session = Depends(get_db), 
                    admin_user: User = Depends(get_admin_user)):
    return crud.restaurant.create_restaurant(db, restaurant_create)

@router.patch("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(restaurant_id: int,
                    restaurant_update: RestaurantUpdate,
                    db: Session = Depends(get_db), 
                    admin_user: User = Depends(get_admin_user)):
    return crud.restaurant.update_restaurant(db, restaurant_id, restaurant_update)

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int,
                    db: Session = Depends(get_db), 
                    admin_user: User = Depends(get_admin_user)):
    crud.restaurant.delete_restaurant(restaurant_id, db)
    return {"detail": "Restaurant deleted"}
    