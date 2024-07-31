import asyncio
import logging
from fastapi import status
from httpx import AsyncClient, Response
from datetime import datetime, timedelta
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func

from src.core.config import settings

from .models import User
from .utils import get_hashed_password, verify_password, generate_secure_password

logger = logging.getLogger(__name__)


# Authenticate a user based on username/email and password
async def authenticate_user(db_session: AsyncSession, login_identifier: str, password: str) -> Optional[User]:
    """
    Authenticate a user based on their username/email and password.

    :param db_session: Database session for executing queries.
    :param login_identifier: The login identifier, either username or email.
    :param password: The user's password.
    :return: User object if authenticated, otherwise None.
    """
    await asyncio.sleep(0.1)  # mitigate user enumeration attacks

    user = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)

    if user and await verify_password(plain_password=password, hashed_password=user.password):
        return user
    
    return None

# Get a user with either email or username provided
async def get_user_by_login_identifier(db_session: AsyncSession, *, login_identifier: str) -> Optional[User]:
    """
    Retrieve a user by their login identifier (username or email).

    :param db_session: Database session for executing queries.
    :param login_identifier: The login identifier, either username or email.
    :return: User object if found, otherwise None.
    """
    query = select(User).where(or_(User.email == login_identifier, User.username == login_identifier))
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

# Get a user using their email
async def get_user_by_email(db_session: AsyncSession, *, email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.

    :param db_session: Database session for executing queries.
    :param email: The user's email address.
    :return: User object if found, otherwise None.
    """
    query = select(User).where(and_(User.email == email, User.is_deleted.is_(False)))
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

# Create a user from Google credentials
async def create_user_from_google_credentials(db_session: AsyncSession, **kwargs) -> User:
    """
    Create a user using Google credentials.

    :param db_session: Database session for executing queries.
    :param kwargs: Additional keyword arguments containing user information.
    :return: Newly created User object.
    """
    password = await generate_secure_password(20)
    hashed_password = await get_hashed_password(password=password)

    user = User(
        username=kwargs.get("email"),  # using the Google email as username
        email=kwargs.get("email"),
        first_name=kwargs.get("given_name"),
        last_name=kwargs.get("family_name"),
        user_image=kwargs.get("picture"),
        password=hashed_password,
    )
    db_session.add(user)
    await db_session.commit()
    return user

# Verify the auth token received by client after Google sign-in
async def verify_google_token(google_access_token: str) -> Optional[dict[str, str]]:
    """
    Verify the Google authentication token.

    :param google_access_token: Google access token received after sign-in.
    :return: User information dictionary if verified, otherwise None.
    """
    async with AsyncClient() as client:
        try:
            response: Response = await client.get(f"{settings.GOOGLE_USERINFO_URL}?access_token={google_access_token}")
            response.raise_for_status()
            user_info: dict[str, str] = response.json()
        except Exception as e:
            logger.error(f"Failed to verify Google token: {e}")
            return None

    if {"email", "given_name", "family_name"}.issubset(user_info):
        return user_info
    
    return None

# Update user's last login time
async def update_user_last_login(db_session: AsyncSession, *, user: User) -> None:
    """
    Update the user's last login time.

    :param db_session: Database session for executing queries.
    :param user: User object to be updated.
    """
    user.last_login = func.now()
    await db_session.commit()
    logger.debug(f"Updated last login time for user {user.id}")
