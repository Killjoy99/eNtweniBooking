from database.core import Base
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

# from product.models import Product


class Organisation(Base):
    __tablename__ = "organisations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(default=None)
    description: Mapped[str] = mapped_column(nullable=True)
    logo_url: Mapped[str] = mapped_column(nullable=True)  # organisation logo
    image_url: Mapped[str] = mapped_column(nullable=True)  # image for the organisation
    default: Mapped[bool] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)  # redefine for indexing
    # users: Mapped[List[User]] = relationship()
    # products: Mapped[List["Product"]] = relationship(back_populates="organisations")
    # bookings: Mapped[List[Booking]] = relationship()

    # Indexes
    __table_args__ = (
        Index(
            "idx_organisation_on_name_description",
            "name",
            "description",
            postgresql_concurrently=True,
        ),
        Index(
            "idx_organisation_on_name_description",
            "name",
            "description",
            postgresql_concurrently=True,
            postgresql_where=(active.is_(True)),
        ),
    )

    class Config:
        from_attributes = True
