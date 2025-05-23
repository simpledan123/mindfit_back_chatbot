from sqlalchemy.orm import Session

from models.restaurant import Restaurant
from schemas.restaurant import RestaurantCreate, RestaurantUpdate

def get_restaurant(db: Session, restaurant_id: int):
     return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

def create_restaurant(db: Session, restaurant_create: RestaurantCreate):
     db_restaurant = Restaurant(
          name=restaurant_create.name,
          address=restaurant_create.address,
          phone=restaurant_create.phone,
          latitude=restaurant_create.latitude,
          longitude=restaurant_create.longitude
     )
     db.add(db_restaurant)
     db.commit()
     db.refresh(db_restaurant)
     return db_restaurant

def update_restaurant(db: Session, restaurant_id: int, restaurant_update: RestaurantUpdate):
     db_restaurant = get_restaurant(db, restaurant_id)
     update_data = restaurant_update.model_dump(exclude_unset=True)
     for key, value in update_data.items():
         setattr(db_restaurant, key, value)
     db.commit()
     db.refresh(db_restaurant)
     return db_restaurant

def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = get_restaurant(db, restaurant_id)
    db.delete(db_restaurant)
    db.commit()