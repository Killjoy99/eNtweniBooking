from pydantic import Field
from typing import Optional, List

from src.core.schemas import CustomBaseModel


class ProductBase(CustomBaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    price: Optional[float]
    unit_of_measure: Optional[str]
    slug: Optional[str]
    organisation_id: Optional[int]


class ProductCreate(ProductBase):
    pass


# class ProductUpdate(CustomBaseModel):
#     description: Optional[str] = Field(None, nullable=True)
#     default: Optional[bool] = Field(False, nullable=True)
#     # banner_enabled: Optional[bool] = Field(False, nullable=True)
#     # banner_color: Optional[str] = Field(None, nullable=True)
#     # banner_text: Optional[NameStr] = Field(None, nullable=True)


class ProductRead(ProductBase):
    id: Optional[int]
    slug: Optional[str]
    name: Optional[str]
    description: str


# class ProductPagination(Pagination):
#     items: List[ProductRead] = []