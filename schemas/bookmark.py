from pydantic import BaseModel
from .restaurant import RestaurantRead

class BookmarkCreate(BaseModel):
    restaurant_id: int

class BookmarkRead(RestaurantRead):
    pass
    
