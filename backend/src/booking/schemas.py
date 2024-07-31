from pydantic import Field, BaseModel
from typing import Optional, List


class BookingBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None)
    default: Optional[bool] = Field(False)
    unit_of_measure: Optional[str]
    slug: Optional[str]
    # organisation_id: Optional[int]


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