import logging
import jwt
from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request, Response, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
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
)
from .utils import create_access_token, create_refresh_token, get_current_user
from httpx import AsyncClient

logger = logging.getLogger(__name__)

auth_router = APIRouter(tags=["Authentication"])


@auth_router.get("/me", name="me")
async def get_me(request: Request, db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db), is_template: Optional[bool] = Depends(check_accept_header)):
    if is_template:
        return render_template(request=request, template_name="me.html")
    else:
        return return_json(data={"message": "Return the logged in user"})


@auth_router.get("/login", summary="Login template frontend", name="sign_in")
async def login(request: Request, is_template: Optional[bool]=Depends(check_accept_header)):
    if is_template:
        data = {}
        return render_template(request=request, template_name="auth/login.html", context={"data": data})
    else:
        data = {}
        return return_json(data=data)


@auth_router.get("/google-login/", summary="Redirect to Google OAuth2 login", name="google_login")
async def google_login():
    google_auth_url = (
        f"{settings.GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)


@auth_router.get("/callback", summary="Handle Google OAuth2 callback", name="callback")
async def callback(request: Request, db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

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
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none", secure=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="none", secure=True)
        return response


@auth_router.post("/login/", summary="Create access and refresh tokens for user", name="login")
async def login(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    is_template: Optional[bool]=Depends(check_accept_header),
    db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends(None)
    ):
    
    login_identifier, password = form_data.username.lower(), form_data.password
    
    try:
        user: User | None = await authenticate_user(db_session=db_session, login_identifier=login_identifier, password=password)
        
        if not user:
            if is_template:
                return render_template(request=request, template_name="login.html", error_message="Incorrect email/user or password")
            else:
                return JSONResponse(status_code=400, content={"error": "Incorrect email/user or password"})
        
        access_token = await create_access_token(login_identifier, user_data={"user_id": user.id, "username": user.username, "email": user.email, "image": user.user_image})
        refresh_token = await create_refresh_token(login_identifier, user_data={"user_id": user.id, "username": user.username, "email": user.email, "image": user.user_image})
            
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none", secure=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="none", secure=True)
            
        background_tasks.add_task(update_user_last_login, db_session, user=user)
        return RedirectResponse(url="/api/v1/home", status_code=status.HTTP_302_FOUND)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post("/refresh/", summary="Create a new access token for the user", name="refresh")
async def get_new_access_token_from_refresh_token(
    refresh_token: Annotated[str, Cookie()],
    response: Response,
    db_session: async_sessionmaker[AsyncSession] = Depends(get_async_db),
):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
        login_identifier = payload.get("sub")
        if not login_identifier:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        user = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not active",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_access_token = create_access_token(
            login_identifier, expires_delta=timedelta(minutes=settings.NEW_ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        response.set_cookie(key="access_token", value=new_access_token, httponly=True, samesite="none", secure=True)

        return "Access token has been successfully refreshed"


@auth_router.post("/logout/", summary="Logout by removing http-only cookies", name="logout")
async def logout(request: Request, response: Response, current_user: User = Depends(get_current_user)):
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
