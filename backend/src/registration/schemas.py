from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserRegistrationSchema(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    uploaded_image: Optional[str] = None
