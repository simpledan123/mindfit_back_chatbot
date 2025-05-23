from typing import List
from typing import TYPE_CHECKING
from enum import Enum
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from .bookmark import bookmark_table

if TYPE_CHECKING:
    from .restaurant import Restaurant
    from .review import Review

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")
    summary: Mapped["UserSummary"] = relationship("UserSummary", back_populates="user", uselist=False)
    keywords: Mapped[List["UserKeyword"]] = relationship("UserKeyword", back_populates="user")


    bookmarked_restaurants: Mapped[List["Restaurant"]] = relationship("Restaurant", secondary=bookmark_table)
