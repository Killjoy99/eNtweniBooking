from typing import Optional

from pydantic import BaseModel


class UserRegistrationSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    uploaded_image: Optional[str] = None
