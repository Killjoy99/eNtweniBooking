import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.services import get_user_by_login_identifier
from src.core.utils import check_accept_header, templates
from src.database.core import get_async_db

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


@account_router.post("/register/", summary="Register a new User", name="register")
async def register_user(
    request: Request,
    background_tasks: BackgroundTasks,
    is_template: Optional[bool] = Depends(check_accept_header),
    db_session: AsyncSession = Depends(get_async_db),
):
    """Register a new user and handle image upload if provided."""
    user_schema: Optional[UserRegistrationSchema] = None

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

        if not user_schema:
            raise HTTPException(status_code=400, detail="Invalid registration data")

        # Check if the user already exists
        existing_user_by_email = await get_user_by_login_identifier(
            db_session=db_session, login_identifier=user_schema.email
        )
        existing_user_by_username = await get_user_by_login_identifier(
            db_session=db_session,
            login_identifier=user_schema.username,
        )
        if existing_user_by_email or existing_user_by_username:
            if is_template:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with provided credentials already exists",
                )
            else:
                return JSONResponse(
                    content={
                        "status_code": status.HTTP_409_CONFLICT,
                        "detail": "User with provided credentials already exists",
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

        # Redirect to login page
        if is_template:
            return RedirectResponse(
                url=request.url_for("sign_in"), status_code=status.HTTP_302_FOUND
            )
        else:
            return JSONResponse(
                content={
                    "status_code": status.HTTP_201_CREATED,
                    "detail": "User Created Successfully",
                }
            )

    except HTTPException as http_exc:
        raise http_exc  # Re-raise known HTTP exceptions
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
