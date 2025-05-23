from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

if TYPE_CHECKING:
    from .review import Review

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)

    review_id = Column(Integer, ForeignKey("reviews.id"))
    review = relationship("Review", back_populates="images")
