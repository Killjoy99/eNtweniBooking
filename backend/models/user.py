from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    remember_me: bool