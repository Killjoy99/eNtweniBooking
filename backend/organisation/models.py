from slugify import slugify
from pydantic import Field
from pydantic.color import Color

from typing import Optional, List

from sqlalchemy.event import listen
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy_utils import TSVectorType

from backend.database.core import Base
from backend.models import EntweniBookingBase, NameStr, OrganisationSlug, PrimaryKey, Pagination


class Organisation(Base):
    __table_args__ = {"schema": "entwenibooking_core"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    slug = Column(String)
    default = Column(Boolean)
    description = Column(String)
    banner_enabled = Column(Boolean)
    banner_color = Column(String)
    banner_text = Column(String)
    
    search_vector = Column(TSVectorType("name", "description", weights={"name": "A", "description": "B"}))
    

def generate_slug(target, value, oldvalue, initiator):
    """Creates a reasonable slug based on Organisation name."""
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value, separator="_")
        

listen(Organisation.name, "set", generate_slug)


class OrganisationBase(EntweniBookingBase):
    id: Optional[PrimaryKey]
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    banner_enabled: Optional[bool] = Field(False, nullable=True)
    banner_color: Optional[Color] = Field(None, nullable=True)
    banner_text: Optional[NameStr] = Field(None, nullable=True)


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(EntweniBookingBase):
    id: Optional[PrimaryKey]
    description: Optional[str] = Field(None, nullable=True)
    default: Optional[bool] = Field(False, nullable=True)
    banner_enabled: Optional[bool] = Field(False, nullable=True)
    banner_color: Optional[Color] = Field(None, nullable=True)
    banner_text: Optional[NameStr] = Field(None, nullable=True)


class OrganizationRead(OrganizationBase):
    id: Optional[PrimaryKey]
    slug: Optional[OrganizationSlug]


class OrganizationPagination(Pagination):
    items: List[OrganizationRead] = []