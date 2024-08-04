import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.services import get_user_by_login_identifier
from src.core.decorators import check_accept_header, render_template, return_json
from src.database.core import get_async_db

from .schemas import UserRegistrationSchema
from .services import ImageSaver, create_user

logger = logging.getLogger(__name__)

account_router = APIRouter(tags=["Account"])


@account_router.get(
    "/register", summary="Endpoint for the frontend template", name="signup"
)
@render_template(template_name="auth/signup.html")
async def register(
    request: Request,
    is_template: Optional[bool] = Depends(check_accept_header),
    db_session: AsyncSession = Depends(get_async_db),
):
    """Render the user registration template."""
    if is_template:
        return {"data": {}, "error_message": None}
    else:
        return return_json(data={})


@account_router.post("/register/", summary="Register a new User", name="register")
async def register_user(
    request: Request,
    background_tasks: BackgroundTasks,
    is_template: Optional[bool] = Depends(check_accept_header),
    db_session: AsyncSession = Depends(get_async_db),
):
    """Register a new user and handle image upload if provided."""
    user_schema: Optional[UserRegistrationSchema] = None

    if is_template:
        # Handle form data
        form = await request.form()
        user_schema = UserRegistrationSchema(
            username=form.get("username"),
            email=form.get("email"),
            password=form.get("password"),
            first_name=form.get("first_name"),
            last_name=form.get("last_name"),
            uploaded_image=form.get("uploaded_image"),
        )
    else:
        # Handle JSON data
        user_schema = UserRegistrationSchema(**await request.json())

    if not user_schema:
        raise HTTPException(status_code=400, detail="Invalid registration data")

    try:
        # Check if the user already exists
        if await get_user_by_login_identifier(
            db_session=db_session, login_identifier=user_schema.email
        ) or await get_user_by_login_identifier(
            db_session=db_session,
            login_identifier=user_schema.username,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with provided credentials already exists",
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
        return RedirectResponse(
            url=request.url_for("sign_in"), status_code=status.HTTP_302_FOUND
        )

    except HTTPException as http_exc:
        raise http_exc  # Re-raise known HTTP exceptions
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
