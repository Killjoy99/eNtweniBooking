from pydantic import BaseModel
from pydantic import EmailStr, Field, field_validator, BaseModel
from typing import Optional, List


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    # organisation_id: int
    

class UserLoginSchema(BaseModel):
    login_identifier: str
    password: str
    
    
class UserUpdateSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    

class UserReadSchema(BaseModel):
    username: str
    email: EmailStr


class GoogleLoginSchema(BaseModel):
    access_token: str
    

class UserLoginResponseSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    settings: dict
    user_image: str | None
    # role: List[Roles]
    
    class Config:
        from_attribute = True
        
    @classmethod
    def add_image_host(cls, image_url: str | None) -> str:
        if image_url:
            if "/static/" in image_url and settings.ENVIRONMENT == "development":
                return settings.STATIC_HOST + image_url
        return image_url
