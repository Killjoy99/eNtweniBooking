from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.database.core import get_async_db
from src.core.decorators import render_template, return_json, check_accept_header
from src.auth.utils import decode_access_token, decode_refresh_token



home_router = APIRouter(tags=["Home"])


@home_router.get("/home", name="home")
@render_template(template_name="home.html")
async def home(request: Request, response: Response, db_session: AsyncSession = Depends(get_async_db), is_template: Optional[bool] = Depends(check_accept_header)):
    if is_template:
        return {"data": {}, "error_message": None}