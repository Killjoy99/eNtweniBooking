
from typing import Any, Dict, Optional
from pydantic import BaseModel

    
    
class BookingCreate(BaseModel):
    id: Any
    name: Any
    description: Any
    default: Any
    unit_of_measure: Any
    slug: Any

class HTTPValidationError(BaseModel):
    detail: Any

class OrganisationCreateSchema(BaseModel):
    name: Any
    description: Any
    default: Any
    slug: Any

class OrganisationDeactivateSchema(BaseModel):
    name: Any
    slug: Any
    active: Any

class OrganisationUpdateSchema(BaseModel):
    description: Any
    default: Any

class ValidationError(BaseModel):
    loc: Any
    msg: Any
    type: Any
