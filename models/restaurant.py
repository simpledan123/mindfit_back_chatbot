from typing import List
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base

if TYPE_CHECKING:
    from .review import Review

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    address: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(10), nullable=True)
    latitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="restaurant")