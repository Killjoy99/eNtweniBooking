from pydantic import Field
from pydantic.color import Color
from typing import Optional, List

from core.schemas import CustomBaseModel #, NameStr, OrganisationSlug, PrimaryKey, Pagination


class OrganisationBase(CustomBaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    slug: Optional[str] = Field(nullable=True)
    # banner_enabled: Optional[bool] = Field(False, nullable=True)
    # banner_color: Optional[Color] = Field(None, nullable=True)
    # banner_text: Optional[NameStr] = Field(None, nullable=True)


class OrganisationCreate(CustomBaseModel):
    name: str
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    slug: Optional[str] = Field(nullable=True)


# class OrganisationUpdate(CustomBaseModel):
#     description: Optional[str] = Field(None, nullable=True)
#     default: Optional[bool] = Field(False, nullable=True)
#     # banner_enabled: Optional[bool] = Field(False, nullable=True)
#     # banner_color: Optional[str] = Field(None, nullable=True)
#     # banner_text: Optional[NameStr] = Field(None, nullable=True)


class OrganisationRead(OrganisationBase):
    id: Optional[int]
    slug: Optional[str]


# class OrganisationPagination(Pagination):
#     items: List[OrganisationRead] = []