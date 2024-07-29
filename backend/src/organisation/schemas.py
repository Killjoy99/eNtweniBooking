from pydantic import Field
from pydantic.color import Color
from typing import Optional, List

from src.core.schemas import CustomBaseModel #, NameStr, OrganisationSlug, PrimaryKey, Pagination


class OrganisationBase(CustomBaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    slug: Optional[str] = Field(nullable=True)
    

class OrganisationCreateSchema(CustomBaseModel):
    name: str
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    slug: Optional[str] = Field(nullable=True)


class OrganisationUpdateSchema(CustomBaseModel):
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)


class OrganisationReadSchema(OrganisationBase):
    id: Optional[int]
    slug: Optional[str]
    
    
class OrganisationDeactivateSchema(CustomBaseModel):
    name: str
    slug: str
    active: bool


# class OrganisationPagination(Pagination):
#     items: List[OrganisationRead] = []