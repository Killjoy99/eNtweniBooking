import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.utils import get_hashed_password

from .schemas import UserRegistrationSchema

logger = logging.getLogger(__name__)


DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte (1Mb)


async def create_user(
    db_session: AsyncSession, *, user_schema: UserRegistrationSchema
) -> User:
    hashed_password = await get_hashed_password(user_schema.password)
    new_user = User(
        username=user_schema.username.lower(),
        email=user_schema.email.lower(),
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        password=hashed_password,
    )

    db_session.add(new_user)
    await db_session.commit()

    return new_user


class ImageSaver:
    @classmethod
    def save_user_image(cls, user, uploaded_image):
        pass
