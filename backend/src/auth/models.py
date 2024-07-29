import string
import secrets
import bcrypt
import jwt

from typing import List, Optional
from datetime import datetime, timedelta

from pydantic import validator, Field
from pydantic.networks import EmailStr

from sqlalchemy import ForeignKey, func, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.config import (
    JWT_ACCESS_SECRET_KEY,
    ENCRYPTION_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

from src.core.enums import UserRoles
from src.core.models import TimeStampMixin
from src.core.schemas import OrganisationSlug, Pagination, PrimaryKey, CustomBaseModel

from src.database.core import Base
# from src.organisation.models import Organisation
# from backend.product.models import Product, ProductRead


# def generate_password():
#     """Generates a reasonable password if none is provided"""
#     alphanumeric = string.ascii_letters + string.digits
#     while True:
#         password = "".join(secrets.choice(alphanumeric) for i in range(16))
#         if(any(c.islower() for c in password) and any(c.isupper() for c in password) and sum(c.isdigit() for c in password) >= 3): # noqa
#             break
#     return password


# def hash_password(password: str) -> str:
#     """Generates a hashed version of the provided password"""
#     pw = bytes(password, "utf-8")
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(pw, salt=salt)


# class EntweniBookingUser(Base, TimeStampMixin):
#     __table_args__ = {"schema": "entwenibooking_core"}
    
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True)
#     password = Column(LargeBinary, nullable=False)
#     last_mfa_time = Column(DateTime, nullable=True)
#     experimental_features = Column(Boolean, default=False)
    
#     # relationships
#     # events = relationship("Event", backref="dispatch_user")

#     # search_vector = Column(
#     #     TSVectorType("email", regconfig="pg_catalog.simple", weights={"email": "A"})
#     # )
    
#     def check_password(self, password):
#         return bcrypt.checkpw(password.encode("utf-8"), self.password)
    
#     @property
#     def token(self):
#         now = datetime.utcnow()
#         exp = (now + timedelta(seconds=ENTWENIBOOKING_JWT_EXP)).timestamp()
#         data = {
#             "exp": exp,
#             "email": self.email
#         }
#         return jwt.encode(data, ENTWENIBOOKING_JWT_SECRET, algorithm=ENTWENIBOOKING_JWT_ALG)
    
#     def get_organisation_role(self, organisation_slug: OrganisationSlug):
#         """Gets a user's role for a given organisation slug"""
#         for o in self.organisations:
#             if o.organisation.slug == organisation_slug:
#                 return o.role
            
            
# class EntweniBookingUserOrganisation(Base, TimeStampMixin):
#     __table_args__ = {"schema": "entwenibooking_core"}
#     entwenibooking_user_id = Column(Integer, ForeignKey(EntweniBookingUser.id), primary_key=True)
#     entwenibooking_user = relationship(EntweniBookingUser, backref="organisations")
    
#     organisation_id = Column(Integer, ForeignKey(Organisation.id), primary_key=True)
#     organisation = relationship(Organisation, backref="users")
    
#     role = Column(String, default=UserRoles.member)
    
    
# class UserOrganisation(CustomBaseModel):
#     organisation = OrganizationRead
#     default: Optional[bool] = False
#     role: Optional[str] = Field(None, nullable=True)
    
    
# class UserBase(CustomBaseModel):
#     email = EmailStr
#     organisations: Optional[List[UserOrganisation]] = []
    
#     @validator
#     def email_required(cls, v):
#         if not v:
#             raise ValueError("Must not be an empty string and must be an email")
#         return v
    
    
# class UserLogin(UserBase):
#     password: str
    
#     @validator("password")
#     def password_required(cls, v):
#         if not v:
#             raise ValueError("Must not be an empty string")
#         return v


# class UserRegister(UserLogin):
#     password: Optional[str] = Field(None, nullable=True)
    
#     @validator("password", pre=True, always=True)
#     def password_required(cls, v):
#         """Generate passwords for those that don't have one."""
#         password = v or generate_password()
#         return hash_password(password=password)
    

# class UserLoginResponse(CustomBaseModel):
#     token: Optional[str] = Field(None, nullable=True)
    

# class UserRead(UserBase):
#     id: PrimaryKey
#     role: Optional[str] = Field(None, nullable=True)
#     experimental_features: Optional[bool]
    

# class UserUpdate(CustomBaseModel):
#     id: PrimaryKey
#     password: Optional[str] = Field(None, nullable=True)

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    # experimental_features: Mapped[bool] = mapped_column(default=False)
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)
    
    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        data = {
            "exp": exp,
            "email": self.email
        }
        return jwt.encode(data, JWT_ACCESS_SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)
    
    