from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.core.schemas import OrganisationSlug

from src.auth.routers import auth_router, user_router
from src.organisation.routers import organisation_router
from src.booking.routers import booking_router
from src.product.routers import product_router


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


api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(organisation_router, prefix="/organisations", tags=["organisation"])
api_router.include_router(booking_router, prefix="/bookings", tags=["bookings"])
api_router.include_router(product_router, prefix="/products", tags=["products"])

# NOTE: Other routers go here below in order

@api_router.get("/healthcheck", name="healthcheck", tags=["healthcheck"])
async def healthcheck():
    return {"status", "ok"}

# api_router.include_router(authenticated_organisation_api_router, dependencies=[Depends(get_current_user)])

# api_router.include_router(authenticated_api_router, dependencies=[Depends(get_current_user)])
