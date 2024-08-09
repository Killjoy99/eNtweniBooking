import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from core.utils import check_accept_header, templates
from database.core import get_async_db
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_limiter.depends import RateLimiter
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .config import auth_settings
from .schemas import UserLoginSchema
from .services import (
    authenticate_user,
    create_user_from_google_credentials,
    get_current_user,
    get_user_by_email,
    get_user_by_login_identifier,
    update_user_last_login,
    verify_google_token,
)
from .utils import create_access_token, create_refresh_token, set_cookies_and_json

# TODO: Re-implement jwt, module has changed (Breaking change)

logger = logging.getLogger(__name__)

auth_router = APIRouter(tags=["Authentication"])


@auth_router.get("/me", name="me")
async def get_me(
    request: Request,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
    user: UserLoginSchema = Depends(get_current_user),
):
    """Return the logged-in user's information."""
    user_info = {"message": "Return the logged-in user"}
    if is_template:
        return templates.TemplateResponse(
            "me.html", {"request": request, "user": user_info}
        )
    return JSONResponse(content={"data": user_info, "error_message": None})


@auth_router.get("/login", summary="Login template frontend", name="sign_in")
def login_page(
    request: Request, is_template: Optional[bool] = Depends(check_accept_header)
):
    """Render the login page."""
    if is_template:
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "data": {}}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@auth_router.post(
    "/login/",
    summary="Create access and refresh tokens for user",
    name="login",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def login(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Authenticate user and create access and refresh tokens."""
    login_schema = None
    if is_template:
        form = await request.form()
        login_schema = UserLoginSchema(
            login_identifier=form.get("login_identifier"),  # type: ignore
            password=form.get("password"),  # type: ignore
        )
    else:
        data = await request.json()
        login_schema = UserLoginSchema(**data)

    if not login_schema:
        raise HTTPException(
            status_code=400, detail="Login identifier and password required"
        )

    try:
        user = await authenticate_user(
            db_session=db_session,
            login_identifier=login_schema.login_identifier,
            password=login_schema.password,
        )

        if not user:
            error_message = "Incorrect Username or Password"
            if is_template:
                return templates.TemplateResponse(
                    "auth/login.html",
                    {
                        "request": request,
                        "error_message": error_message,
                        "data": login_schema.model_dump(),
                    },
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            return JSONResponse(
                content={"detail": error_message},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        access_token = await create_access_token(
            login_schema.login_identifier,
            user_data={
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "image": user.user_image,
            },
        )
        refresh_token = await create_refresh_token(
            login_schema.login_identifier,
            user_data={
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "image": user.user_image,
            },
        )

        # Debugging cookies
        logger.debug(f"Setting access_token cookie: {access_token}")
        logger.debug(f"Setting refresh_token cookie: {refresh_token}")

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax",  # Adjust as needed
            secure=False,  # Adjust for production
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",  # Adjust as needed
            secure=False,  # Adjust for production
        )

        background_tasks.add_task(update_user_last_login, db_session, user=user)

        if is_template:
            return RedirectResponse(
                url=request.url_for("home"), status_code=status.HTTP_302_FOUND
            )
        else:
            return JSONResponse(
                content={
                    "status_code": status.HTTP_202_ACCEPTED,
                    "detail": "LOGIN_SUCCESS",
                }
            )

    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.get(
    "/google-login/", summary="Redirect to Google OAuth2 login", name="google_login"
)
async def google_login():
    """Redirect to Google OAuth2 login."""
    google_auth_url = (
        f"{auth_settings.GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={auth_settings.GOOGLE_CLIENT_ID}&redirect_uri={auth_settings.REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)


@auth_router.get("/callback", summary="Handle Google OAuth2 callback", name="callback")
async def callback(request: Request, db_session: AsyncSession = Depends(get_async_db)):
    """Handle Google OAuth2 callback and authenticate user."""
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    try:
        async with AsyncClient() as client:
            token_response = await client.post(
                auth_settings.GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": auth_settings.GOOGLE_CLIENT_ID,
                    "client_secret": auth_settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": auth_settings.REDIRECT_URI,
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
                user = await create_user_from_google_credentials(
                    db_session=db_session, **user_info
                )
            else:
                await update_user_last_login(db_session, user=user)

            access_token = await create_access_token(email)
            refresh_token = await create_refresh_token(email)

            response = RedirectResponse(url="/")
            await set_cookies_and_json(response, access_token, refresh_token)
            return response

    except Exception as e:
        logger.error(f"Error during Google OAuth2 callback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post(
    "/refresh/", summary="Create a new access token for the user", name="refresh"
)
async def get_new_access_token_from_refresh_token(
    refresh_token: Annotated[str, Cookie()],
    response: Response,
    db_session: AsyncSession = Depends(get_async_db),
):
    """Create a new access token from the refresh token."""
    try:
        payload = jwt.decode(
            refresh_token,
            auth_settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[auth_settings.ENCRYPTION_ALGORITHM],
        )
        login_identifier = payload.get("sub")
        if not login_identifier:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        user = await get_user_by_login_identifier(
            db_session, login_identifier=login_identifier
        )
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active"
            )

        new_access_token = await create_access_token(
            login_identifier,
            expires_delta=timedelta(
                minutes=auth_settings.NEW_ACCESS_TOKEN_EXPIRE_MINUTES
            ),  # type: ignore
        )

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="none",
            secure=True,
        )
        return "Access token has been successfully refreshed"

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token"
        )
    except jwt.PyJWTError:
        logger.error(f"Error decoding refresh token: {refresh_token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@auth_router.post(
    "/logout/", summary="Logout by removing http-only cookies", name="logout"
)
async def logout(
    request: Request,
    response: Response,
    current_user: UserLoginSchema = Depends(get_current_user),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Logout the user by removing http-only cookies."""
    expires = datetime.now(timezone.utc) + timedelta(seconds=1)
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
    if is_template:
        return RedirectResponse(url=request.url_for("sign_in"))
    return JSONResponse(status_code=200, content={"message": "Successfully logged out"})
