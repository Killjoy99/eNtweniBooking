import logging

from auth.models import User
from auth.utils import generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserRegistrationSchema

logger = logging.getLogger(__name__)


DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte (1Mb)


async def create_user(
    db_session: AsyncSession, *, user_schema: UserRegistrationSchema
) -> User:
    hashed_password = await generate_password_hash(user_schema.password)
    new_user = User(
        username=user_schema.username.lower(),
        email=user_schema.email.lower(),
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        password=hashed_password,
    )

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return new_user


class ImageSaver:
    @classmethod
    def save_user_image(cls, user, uploaded_image):
        pass
