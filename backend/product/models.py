from typing import Optional, List
from pydantic.color import Color

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base


class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str]
    default: Mapped[bool]
    description: Mapped[str]
    price: Mapped[float]
    unit_of_measure: Mapped[str]
    # banner_enabled: Mapped[bool]
    # banner_color: Mapped[str]
    # banner_text: Mapped[str]