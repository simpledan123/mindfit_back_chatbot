from sqlalchemy import Table, Column, ForeignKey, Integer
from db.database import Base

bookmark_table = Table(
    "bookmarks",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("restaurant_id", ForeignKey("restaurants.id", ondelete="CASCADE"), primary_key=True),
)