from sqlalchemy.orm import Mapped, mapped_column

from src.database.core import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str]
    default: Mapped[bool]
    description: Mapped[str]
    price: Mapped[float]
    unit_of_measure: Mapped[str]
    # organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))
    # organisation: Mapped["Organisation"] = relationship()
    # booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    # booking: Mapped["Booking"] = relationship()
