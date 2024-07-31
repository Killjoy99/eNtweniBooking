import string
import secrets
import bcrypt
import jwt

from typing import List, Optional
from datetime import datetime, timedelta

from pydantic import validator, Field
from pydantic.networks import EmailStr

from sqlalchemy import ForeignKey, func, String, Boolean, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.core.enums import UserRoles

from src.database.core import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), default="")
    last_name: Mapped[str] = mapped_column(String(150), default="")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    user_image: Mapped[str] = mapped_column(String(1048), nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)        #redefine column for indexing
    experimental_features: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self):
        return f"{self.username}"
    
    # Indexes
    __table_args__ = (
        Index("idx_user_on_email_username", "email", "username", postgresql_concurrently=True),
        Index(
            "idx_user_on_email_username",
            "email",
            "username",
            postgresql_concurrently=True,
            postgresql_where=(is_deleted.is_(False))
        ),
    )