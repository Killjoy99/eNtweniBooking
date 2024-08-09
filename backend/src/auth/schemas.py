from core.config import settings
from pydantic import BaseModel, EmailStr


class GoogleLoginSchema(BaseModel):
    access_token: str


class UserLoginSchema(BaseModel):
    login_identifier: str
    password: str
    # @field_validator("password", mode="after")
    # @classmethod
    # async def valid_password(cls, password: str) -> str:
    #     if not re.match(STRONG_PASSWORD_PATTERN, password):
    #         raise ValueError(
    #             "Password must contain atleast"
    #             "one lower case character, "
    #             "one upper case character, "
    #             "digit or "
    #             "special symbol"
    #         )

    #     return password


class UserLoginResponseSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    settings: dict
    user_image: str | None
    # role: List[Roles]

    @classmethod
    def add_image_host(cls, image_url: str | None) -> str | None:
        if image_url:
            if "/static/" in image_url and settings.ENVIRONMENT == "development":
                return settings.STATIC_HOST + image_url
        return image_url

    class Config:
        from_attribute = True
