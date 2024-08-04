from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth.routers import auth_router
from src.booking.routers import booking_router
from src.core.routers import home_router
from src.database.core import get_async_db
from src.organisation.routers import organisation_router
from src.product.routers import product_router
from src.registration.routers import account_router

api_router = APIRouter(default_response_class=JSONResponse)


# WARNING: do not use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()

api_router.include_router(home_router)
api_router.include_router(account_router)
api_router.include_router(auth_router)
api_router.include_router(organisation_router)
api_router.include_router(booking_router)
api_router.include_router(product_router)

# NOTE: Other routers go here below in order


@api_router.get("/healthcheck", name="healthcheck", tags=["Healthcheck"])
async def healthcheck(
    db_session: async_sessionmaker[AsyncSession] = Depends(get_async_db),
):
    try:
        return {"status", "ok"}
    except Exception as e:
        return {"status": f"{e}"}


# api_router.include_router(authenticated_organisation_api_router, dependencies=[Depends(get_current_user)])

# api_router.include_router(authenticated_api_router, dependencies=[Depends(get_current_user)])
