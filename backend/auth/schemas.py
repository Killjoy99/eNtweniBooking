from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    organisation: str
    

class UserLogin(BaseModel):
    username: str = "admin" or None
    password: str = "admin123" or None
    
    
class UserUpdate(BaseModel):
    username: str
    password: str
    email: EmailStr
    

class UserRead(BaseModel):
    username: str
    email: EmailStr