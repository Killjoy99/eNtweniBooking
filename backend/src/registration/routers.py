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
    if is_template:
        data = {}
        return {"data": {}, "error_message": None}
    else:
        data = {}
        return return_json(data=data)


# user data and image in one endpoint
# https://github.com/tiangolo/fastapi/issues/2257
# https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi
@account_router.post("/register/", summary="Register a new User", name="register")
async def register_user(
    request: Request,
    background_tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_async_db),
    user_schema: UserRegistrationSchema = Depends(UserRegistrationSchema),
):
    try:
        # Check if the user already exists
        if await get_user_by_login_identifier(
            db_session=db_session,
            login_identifier=user_schema.email or user_schema.username,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with provided credentials already exists",
            )

        # Create a new user
        user: User = await create_user(db_session=db_session, user_schema=user_schema)

        # Handle user image upload if provided
        if uploaded_image := user_schema.uploaded_image:
            image_saver = ImageSaver()
            background_tasks.add_task(image_saver.save_user_image, user, uploaded_image)

        # Redirect to login page with the username and password
        return RedirectResponse(
            url=request.url_for("sign_in"), status_code=status.HTTP_302_FOUND
        )

    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
