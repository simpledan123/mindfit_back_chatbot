from typing import List
from typing import Optional
from pydantic import BaseModel, computed_field, PrivateAttr

from schemas.user import UserRead


class Image(BaseModel):
    id: int
    filename: str

class ReviewRead(BaseModel):
    id: int
    rating: float
    comment: str
    user: Optional[UserRead]

    images: List[Image] = []

    @computed_field
    @property
    def image_urls(self) -> List[str]:
        return [f"http://127.0.0.1:8000/images/original/{img.filename}.webp" for img in self.images]
    
class ReviewCreate(BaseModel):
    rating: float
    comment: str

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None