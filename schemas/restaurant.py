from typing import List
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

from schemas.review import ReviewRead

class RestaurantRead(BaseModel):
    id: int
    name: str
    rating: float
    address: str
    phone: str
    latitude: Decimal
    longitude: Decimal

class RestaurantReadWithReviews(RestaurantRead):
    reviews: List[ReviewRead] = []

class RestaurantCreate(BaseModel):
    name: str
    address: str
    phone: str
    latitude: Decimal
    longitude: Decimal

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    




