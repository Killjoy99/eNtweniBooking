import logging
from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils import check_accept_header, templates
from src.database.core import get_async_db

from .schemas import (
    OrganisationCreateSchema,
    OrganisationDeactivateSchema,
    OrganisationResponseSchema,
    OrganisationUpdateSchema,
)
from .services import (
    delete_organisation,
    get_all,
    get_by_id_filtered,
    get_or_create,
    set_organisation_status,
    update_organisation,
)

logger = logging.getLogger(__name__)

organisation_router = APIRouter(prefix="/organisations", tags=["Organisation"])


@organisation_router.get(
    "",
    # response_model=list[OrganisationResponseSchema],
    name="organisations",
)
async def get_organisations(
    request: Request,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Get all organisations."""
    try:
        organisations = await get_all(db_session=db_session)

        if is_template:
            return templates.TemplateResponse(
                "organisation/list.html",
                {"request": request, "organisations": organisations},
            )

        return {
            "organisations": organisations
        }  # Directly return the list of organisations

    except Exception as e:
        logger.error(f"Error getting organisations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@organisation_router.post("", response_model=OrganisationResponseSchema)
async def create_organisation(
    background_tasks: BackgroundTasks,
    organisation_in: OrganisationCreateSchema,
    db_session: AsyncSession = Depends(get_async_db),
):
    """Create a new organisation."""
    try:
        organisation = await get_or_create(
            db_session=db_session, organisation_in=organisation_in
        )
        # Add background task here if needed
        return organisation

    except Exception as e:
        logger.error(f"Error creating organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@organisation_router.get(
    "/{organisation_id}",
    response_model=OrganisationResponseSchema,
    name="organisation_detail",
)
async def get_organisation(
    request: Request,
    organisation_id: int,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Get an organisation by ID."""
    try:
        organisation = await get_by_id_filtered(
            db_session=db_session, id=organisation_id, active=True
        )

        if not organisation:
            raise HTTPException(status_code=404, detail="Organisation not found")

        if is_template:
            return templates.TemplateResponse(
                "organisation/detail.html",
                {"request": request, "organisation": organisation},
            )

        return {"organisation": organisation}

    except Exception as e:
        logger.error(f"Error getting organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@organisation_router.put(
    "/{organisation_id}",
    response_model=OrganisationResponseSchema,
    name="organisation_update",
)
async def update(
    request: Request,
    organisation_id: int,
    organisation_in: OrganisationUpdateSchema,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Update an organisation."""
    try:
        organisation = await update_organisation(
            db_session=db_session,
            organisation_id=organisation_id,
            organisation_in=organisation_in,
        )

        if is_template:
            return templates.TemplateResponse(
                "organisation/detail.html",
                {"request": request, "organisation": organisation},
            )

        return {"organisation": organisation}

    except Exception as e:
        logger.error(f"Error updating organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@organisation_router.post(
    "/{organisation_id}/deactivate",
    response_model=OrganisationDeactivateSchema,
    name="organisation_deactivate",
)
async def deactivate_organisation(
    request: Request,
    organisation_id: int,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Deactivate an organisation."""
    try:
        organisation = await set_organisation_status(
            db_session=db_session, organisation_id=organisation_id, active=False
        )

        if is_template:
            return RedirectResponse(
                url=request.url_for("organisations"), status_code=status.HTTP_302_FOUND
            )

        return {"organisation": organisation}

    except Exception as e:
        logger.error(f"Error deactivating organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@organisation_router.post(
    "/{organisation_id}/reactivate",
    response_model=OrganisationDeactivateSchema,
    name="organisation_reactivate",
)
async def reactivate_organisation(
    request: Request,
    organisation_id: int,
    db_session: AsyncSession = Depends(get_async_db),
    is_template: Optional[bool] = Depends(check_accept_header),
):
    """Reactivate an organisation."""
    try:
        organisation = await set_organisation_status(
            db_session=db_session, organisation_id=organisation_id, active=True
        )

        if is_template:
            return templates.TemplateResponse(
                "organisation/detail.html",
                {"request": request, "organisation": organisation},
            )

        return {"organisation": organisation}

    except Exception as e:
        logger.error(f"Error reactivating organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@organisation_router.delete(
    "/{organisation_id}/delete", response_model=dict, name="organisation_delete"
)
async def delete(
    request: Request,
    organisation_id: int,
    db_session: AsyncSession = Depends(get_async_db),
):
    """Delete an organisation."""
    try:
        await delete_organisation(
            db_session=db_session, organisation_id=organisation_id
        )
        return {"detail": f"Deleted Organisation with ID: {organisation_id}"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
