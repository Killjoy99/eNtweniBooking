import logging
from typing import Optional

from auth.models import User
from auth.services import get_user_by_login_identifier
from core.utils import check_accept_header, templates
from database.core import get_async_db
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserRegistrationSchema
from .services import ImageSaver, create_user

logger = logging.getLogger(__name__)

account_router = APIRouter(tags=["Account"])


@account_router.get(
    "/register", summary="Endpoint for the frontend template", name="signup"
)
async def register(
    request: Request,
    is_template: Optional[bool] = Depends(check_accept_header),
    db_session: AsyncSession = Depends(get_async_db),
):
    """Render the user registration template."""
    if is_template:
        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={"data": {}, "error_message": None},
        )
    else:
        return JSONResponse(content={})


@account_router.post(
    "/register/",
    summary="Register a new User",
    name="register",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def register_user(
    request: Request,
    background_tasks: BackgroundTasks,
    is_template: Optional[bool] = Depends(check_accept_header),
    db_session: AsyncSession = Depends(get_async_db),
):
    """Register a new user and handle image upload if provided."""
    try:
        if is_template:
            # Handle form data
            form = await request.form()
            user_schema = UserRegistrationSchema(
                username=form.get("username"),  # type: ignore
                email=form.get("email"),  # type: ignore
                password=form.get("password"),  # type: ignore
                first_name=form.get("first_name"),  # type: ignore
                last_name=form.get("last_name"),  # type: ignore
                uploaded_image=form.get("uploaded_image"),  # type: ignore
            )
        else:
            # Handle JSON data
            user_schema = UserRegistrationSchema(**await request.json())

        # Logging for server side events
        logger.info(f"User registration attempted, USERNAME: {user_schema.username}")

        # Check if the user already exists
        existing_user_by_email = await get_user_by_login_identifier(
            db_session=db_session, login_identifier=user_schema.email
        )
        existing_user_by_username = await get_user_by_login_identifier(
            db_session=db_session,
            login_identifier=user_schema.username,
        )

        if existing_user_by_email or existing_user_by_username:
            error_message = "User with provided Username / Email already exists"
            if is_template:
                return templates.TemplateResponse(
                    "auth/signup.html",
                    {
                        "request": request,
                        "error_message": error_message,
                        "data": user_schema.model_dump(),
                    },
                    status_code=status.HTTP_409_CONFLICT,
                )
            else:
                return JSONResponse(
                    content={
                        "status_code": status.HTTP_409_CONFLICT,
                        "detail": error_message,
                    },
                )

        # Create a new user
        user: User = await create_user(db_session=db_session, user_schema=user_schema)

        # Handle user image upload if provided
        if user_schema.uploaded_image:
            image_saver = ImageSaver()
            background_tasks.add_task(
                image_saver.save_user_image, user, user_schema.uploaded_image
            )

        # Success message
        success_message = "Registration successful. Please log in."

        if is_template:
            return templates.TemplateResponse(
                "auth/login.html",
                {
                    "request": request,
                    "success_message": success_message,
                    "data": user_schema.model_dump(),
                },
                status_code=status.HTTP_201_CREATED,
            )
        else:
            return JSONResponse(
                content={
                    "status_code": status.HTTP_201_CREATED,
                    "detail": success_message,
                }
            )

    except HTTPException as http_exc:
        raise http_exc  # Re-raise known HTTP exceptions
    except Exception as e:
        logger.error(f"Error during user registration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
