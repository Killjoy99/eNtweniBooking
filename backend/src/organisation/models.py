from kivy.uix.gridlayout import product
from typing import Optional, List
from pydantic.color import Color

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base

from src.auth.models import User
# from src.product.models import Product
from src.booking.models import Booking


class Organisation(Base):
    __tablename__ = "organisations"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(default=None)
    default: Mapped[bool] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    # users: Mapped[List[User]] = relationship()
    # products: Mapped[List["Product"]] = relationship(back_populates="organisations")
    # bookings: Mapped[List[Booking]] = relationship()