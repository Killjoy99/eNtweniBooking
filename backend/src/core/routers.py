import logging
from typing import Optional

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import decode_access_token, decode_refresh_token
from src.core.decorators import check_accept_header, render_template, return_json
from src.database.core import get_async_db

logger = logging.getLogger(__name__)


home_router = APIRouter(tags=["Home"])


@home_router.get("/home", name="home")
@render_template(template_name="home.html")
async def home(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    if is_template:
        # Get cookies
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        user_info = {}
        error_message = None

        try:
            # Decode the access token to get user information
            if access_token:
                logger.debug(access_token)
                user_info = decode_access_token(access_token)
            elif refresh_token:
                # Optionally, decode the refresh token if access token is not present
                user_info = decode_refresh_token(refresh_token)
            else:
                error_message = "No tokens found in cookies"

        except Exception as e:
            error_message = f"Error decoding tokens: {e}"

        return {"data": {"user_info": user_info}, "error_message": error_message}

    else:
        return return_json(data={})
