from typing import Optional, List
from pydantic.color import Color

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base


class Organisation(Base):
    __tablename__ = "organisations"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(nullable=True)
    default: Mapped[bool] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)