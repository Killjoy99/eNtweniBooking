from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr, AnyHttpUrl
from pydantic.types import conint, constr, SecretStr

# schemas are pydantic models

# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(pattern=r"^[?!\s*$].+", strip_whitespace=True, min_length=3)
OrganisationSlug = constr(pattern=r"^[\w]+(?:_[\w]+)*$", min_length=3)


# Pydantic models...
class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class Pagination(CustomBaseModel):
    itemsPerPage: int
    page: int
    total: int


class PrimaryKeyModel(BaseModel):
    id: PrimaryKey


class ResourceBase(CustomBaseModel):
    resource_type: Optional[str] = Field(None, nullable=True)
    resource_id: Optional[str] = Field(None, nullable=True)
    weblink: Optional[AnyHttpUrl] = Field(None, nullable=True)


class ContactBase(CustomBaseModel):
    email: EmailStr
    name: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    is_external: Optional[bool] = False
    company: Optional[str] = Field(None, nullable=True)
    contact_type: Optional[str] = Field(None, nullable=True)
    notes: Optional[str] = Field(None, nullable=True)
    owner: Optional[str] = Field(None, nullable=True)
