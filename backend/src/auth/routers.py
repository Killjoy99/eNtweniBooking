import logging
import jwt
from datetime import datetime, timedelta
from typing import Optional, Union, Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request, Response, Cookie, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from httpx import AsyncClient

from src.database.core import get_async_db
from src.core.config import settings
from src.core.decorators import check_accept_header, render_template, return_json
from .schemas import UserLoginResponseSchema, GoogleLoginSchema, UserLoginSchema
from .models import User
from .services import (
    authenticate_user,
    create_user_from_google_credentials,
    get_user_by_email,
    get_user_by_login_identifier,
    update_user_last_login,
    verify_google_token,
    get_current_user,
)
from .utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)

auth_router = APIRouter(tags=["Authentication"])

def set_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none", secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="none", secure=True)

@auth_router.get("/me", name="me")
@render_template(template_name="me.html")
async def get_me(
    request: Request,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header)
):
    if is_template:
        return {"data": {}, "error_message": None}
    return return_json(data={"message": "Return the logged-in user"})

@auth_router.get("/login", summary="Login template frontend", name="sign_in")
@render_template(template_name="auth/login.html")
async def login_page(
    request: Request,
    is_template: Optional[bool] = Depends(check_accept_header)
):
    if is_template:
        return {"data": {}, "error_message": None}
    return return_json(data={})

@auth_router.get("/google-login/", summary="Redirect to Google OAuth2 login", name="google_login")
async def google_login():
    google_auth_url = (
        f"{settings.GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)

@auth_router.get("/callback", summary="Handle Google OAuth2 callback", name="callback")
async def callback(
    request: Request,
    db_session: AsyncSession = Depends(get_async_db)
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    try:
        async with AsyncClient() as client:
            token_response = await client.post(
                settings.GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
            )
            token_response.raise_for_status()
            tokens = token_response.json()
            access_token = tokens["access_token"]

            user_info = await verify_google_token(access_token)
            if not user_info:
                raise HTTPException(status_code=400, detail="Invalid token")

            email = user_info.get("email", "").lower()
            if not email:
                raise HTTPException(status_code=400, detail="Email was not provided")

            user = await get_user_by_email(db_session=db_session, email=email)
            if not user:
                user = await create_user_from_google_credentials(db_session=db_session, **user_info)
            else:
                await update_user_last_login(db_session, user=user)

            access_token = await create_access_token(email)
            refresh_token = await create_refresh_token(email)

            response = RedirectResponse(url="/")
            set_cookies(response, access_token, refresh_token)
            return response

    except Exception as e:
        logger.error(f"Error during Google OAuth2 callback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.post("/login/", summary="Create access and refresh tokens for user", name="login")
async def login(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    is_template: Optional[bool] = Depends(check_accept_header),
    db_session: AsyncSession = Depends(get_async_db),
    form_data: Optional[OAuth2PasswordRequestForm] = Depends(None),
    json_data: Optional[UserLoginSchema] = Body(None)
):
    login_identifier, password = None, None

    if form_data:
        login_identifier = form_data.username.lower()
        password = form_data.password
    elif json_data:
        login_identifier = json_data.login_identifier.lower()
        password = json_data.password
    else:
        raise HTTPException(status_code=400, detail="No login credentials provided")

    try:
        user: Optional[User] = await authenticate_user(db_session=db_session, login_identifier=login_identifier, password=password)

        if not user:
            error_message = "Incorrect email/user or password"
            if is_template:
                return {"data": {}, "error_message": error_message}
            return JSONResponse(status_code=400, content={"error": error_message})

        access_token = await create_access_token(login_identifier, user_data={"user_id": user.id, "username": user.username, "email": user.email, "image": user.user_image})
        refresh_token = await create_refresh_token(login_identifier, user_data={"user_id": user.id, "username": user.username, "email": user.email, "image": user.user_image})

        set_cookies(response, access_token, refresh_token)

        background_tasks.add_task(update_user_last_login, db_session, user=user)
        return RedirectResponse(url="/api/v1/home", status_code=status.HTTP_302_FOUND)

    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.post("/refresh/", summary="Create a new access token for the user", name="refresh")
async def get_new_access_token_from_refresh_token(
    refresh_token: Annotated[str, Cookie()],
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
        login_identifier = payload.get("sub")
        if not login_identifier:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        user = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)
        if not user or user.is_deleted:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        new_access_token = await create_access_token(
            login_identifier, expires_delta=timedelta(minutes=settings.NEW_ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        response.set_cookie(key="access_token", value=new_access_token, httponly=True, samesite="none", secure=True)
        return "Access token has been successfully refreshed"

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token")
    except jwt.PyJWTError:
        logger.error(f"Error decoding refresh token: {refresh_token}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

@auth_router.post("/logout/", summary="Logout by removing http-only cookies", name="logout")
async def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user)
):
    expires = datetime.utcnow() + timedelta(seconds=1)
    response.set_cookie(
        key="access_token",
        value="",
        secure=True,
        httponly=True,
        samesite="none",
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )
    response.set_cookie(
        key="refresh_token",
        value="",
        secure=True,
        httponly=True,
        samesite="none",
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )
    return "Cookies removed"
