from typing import List, Optional

from pydantic import BaseModel, Field


class OrganisationBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None)
    default: Optional[bool] = Field(False)
    slug: Optional[str] = Field()


class OrganisationCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(None)
    default: Optional[bool] = Field(False)
    slug: Optional[str] = Field()


class OrganisationUpdateSchema(BaseModel):
    description: Optional[str] = Field(None)
    default: Optional[bool] = Field(False)


class OrganisationReadSchema(OrganisationBase):
    id: int
    slug: str


class OrganisationDeactivateSchema(BaseModel):
    name: str
    slug: str
    active: bool


class OrganisationResponseSchema(BaseModel):
    organisations: List[OrganisationBase]


# class OrganisationPagination(Pagination):
#     items: List[OrganisationRead] = []
