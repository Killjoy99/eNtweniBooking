from pydantic import Field
from typing import Optional, List

from core.schemas import CustomBaseModel


class BookingBase(CustomBaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    unit_of_measure: Optional[str]
    slug: Optional[str]
    # banner_enabled: Optional[bool] = Field(False, nullable=True)
    # banner_color: Optional[Color] = Field(None, nullable=True)
    # banner_text: Optional[NameStr] = Field(None, nullable=True)


class BookingCreate(BookingBase):
    pass


# class BookingUpdate(CustomBaseModel):
#     description: Optional[str] = Field(None, nullable=True)
#     default: Optional[bool] = Field(False, nullable=True)
#     # banner_enabled: Optional[bool] = Field(False, nullable=True)
#     # banner_color: Optional[str] = Field(None, nullable=True)
#     # banner_text: Optional[NameStr] = Field(None, nullable=True)


class BookingRead(BookingBase):
    id: Optional[int]
    slug: Optional[str]
    name: Optional[str]
    description: str


# class BookingPagination(Pagination):
#     items: List[BookingRead] = []