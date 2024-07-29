from typing import Optional, List
from pydantic.color import Color

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base


class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str]
    description: Mapped[str]
    unit_of_measure: Mapped[str]
    # products: Mapped[List["Product"]] = relationship(back_populates="bookings")