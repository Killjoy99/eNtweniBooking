from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models import OrganisationSlug
from auth.routers import auth_router, user_router
# from backend.auth.service import get_current_user


class ErrorMessage(BaseModel):
    msg: str
    

class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]
    
    
api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    }
)


# WARNING: do not use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()

# def get_organisation_path(organisation: OrganisationSlug):
#     pass
# api_router.include_router(auth_router, prefix="/{organisation}/auth", tags=["auth"])


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])

# NOTE: Other routers go here below in order

@api_router.get("/healthcheck", name="healthcheck")
async def healthcheck():
    return {"status", "ok"}

# api_router.include_router(authenticated_organisation_api_router, dependencies=[Depends(get_current_user)])

# api_router.include_router(authenticated_api_router, dependencies=[Depends(get_current_user)])
