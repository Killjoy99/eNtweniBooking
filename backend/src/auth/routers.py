import logging
import jwt

from datetime import datetime
from os import path
from typing import Optional, Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Form, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database.core import get_async_db
from src.core.config import settings
from src.core.decorators import check_accept_header, render_template, return_json

from .schemas import UserLoginResponseSchema, UserCreateSchema, UserLoginSchema, GoogleLoginSchema
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


logger = logging.getLogger(__name__)


auth_router = APIRouter(tags=["Authentication"])


############################## LOGIN / LOGOUT ##########################################
# auth router related
@auth_router.get("/me", name="me")#, response_model=UserRead)
# async def get_me(*, db_session: DbSession, current_user: CurrentUser):
    # return current_user
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

# login post router
@auth_router.post("/google-login/", summary="Login with Google oauth2", name="google_login")
async def login_with_google(
    response: Response,
    google_login_schema: GoogleLoginSchema,
    background_tasks: BackgroundTasks,
    db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db),
):
    google_access_token: str = google_login_schema.access_token
    user_info: dict[str, str] | None = await verify_google_token(google_access_token=google_access_token)
    
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify Google credentials")
    
    # email field is case insensitive, db holds lower case representation of email
    email: str = user_info.get("email", "").lower()
    if not email:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email was not provided")
        
    if not (user := await get_user_by_email(db_session=db_session, email=email)):
        user: User = await create_user_from_google_credentials(db_session=db_session, **user_info)
        
    else:
        # update last login for existing user
        background_tasks.add_task(update_user_last_login, db_session, user=user)
        
    access_token: str = await create_access_token(email)
    refresh_toekn: str = await create_refresh_token(email)
    
    # Send access and refresh token in HTTP only cookiies
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none", secure=True)
    response.set_cookie(key="refresh_toekn", value=refresh_toekn, httponly=True, samesite="none", secure=True)
    
    login_response = UserLoginResponseSchema.model_validate(user)
    return login_response


@auth_router.post("/login/", summary="Create access and refresh tokens for user", name="login")
async def login(response: Response, background_tasks: BackgroundTasks, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db), form_data: OAuth2PasswordRequestForm = Depends()):
    
    # get credentials from a form (frontend)
    if is_template:
        login_identifier, password = form_data.username.lower(), form_data.password
    else:
        login_identifier, password = user.login_identifier, user.password
    
    try:
        user: User | None = await authenticate_user(db_session=db_session, login_identifier=login_identifier, password=password)
    
        # create token based on login identifier instead of static username/email
        access_token: str = await create_access_token(login_identifier)
        refresh_token: str = await create_refresh_token(login_identifier)
        
        logger.debug(f"Access token: {access_token}")
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none", secure=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="none", secure=True)
        
        # update last login
        background_tasks.add_task(update_user_last_login, db_session, user=user)
        
        login_response = UserLoginResponseSchema.model_validate(user)
        return login_response
    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email/user or password")

@auth_router.post("/refresh/", summary="Create a new access token for the user", name="refresh")
async def get_new_access_token_from_refresh_token(
    refresh_token: Annotated[str, Cookie()],
    response: Response,
    db_session: async_sessionmaker[AsyncSession] = Depends(get_async_db),
):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
        login_identifier: str = payload.get("sub")
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
        
        user: User | None = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)

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

# logout router
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
    # this doesn't work, must expire
    # response.delete_cookie("access_token")
    # response.delete_cookie("refresh_token")
    return "Cookies removed"
############################## LOGIN / LOGOUT ##########################################