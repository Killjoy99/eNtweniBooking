from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None)
    default: Optional[bool] = Field(False)
    price: Optional[float]
    unit_of_measure: Optional[str]
    slug: Optional[str]
    organisation_id: Optional[int]


class ProductCreate(ProductBase):
    pass


# class ProductUpdate(CustomBaseModel):
#     description: Optional[str] = Field(None)
#     default: Optional[bool] = Field(False)
#     # banner_enabled: Optional[bool] = Field(False)
#     # banner_color: Optional[str] = Field(None)
#     # banner_text: Optional[NameStr] = Field(None)


class ProductRead(ProductBase):
    id: Optional[int]
    slug: Optional[str]
    name: Optional[str]
    description: str


# class ProductPagination(Pagination):
#     items: List[ProductRead] = []
