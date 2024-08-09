from database.core import Base
from sqlalchemy.orm import Mapped, mapped_column


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str]
    description: Mapped[str]
    unit_of_measure: Mapped[str]
    # products: Mapped[List["Product"]] = relationship(back_populates="bookings")
