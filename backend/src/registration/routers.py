from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Annotated, Optional

from src.core.decorators import check_accept_header, render_template, return_json
from src.database.core import get_async_db
from src.auth.models import User
from src.auth.services import get_user_by_login_identifier

from .schemas import UserRegistrationSchema
from .services import ImageSaver, create_user


account_router = APIRouter(tags=["Account"])


@account_router.get("/register", summary="Endpoint for the frontend template", name="signup")
@render_template(template_name="auth/signup.html")
async def register(request: Request, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
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
    background_tasks: BackgroundTasks,
    db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db),
    user_schema: UserRegistrationSchema = Depends(UserRegistrationSchema),
):
    try:
        # Check if the user already exists
        if await get_user_by_login_identifier(db_session=db_session, login_identifier=user_schema.email or user_schema.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with provided Credentials already exists")
        
        else:
            user: User = await create_user(db_session=db_session, user_schema=user_schema)
            # background_task is executed after the response is sent to the client.
            # this allows to save an image without affecting the user experience.
            if uploaded_image := user_schema.uploaded_image:
                image_saver = ImageSaver(db_session, user=user)
                background_tasks.add_task(image_saver.save_user_image, user, uploaded_image)
                
                return "User has been successfully created"
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    