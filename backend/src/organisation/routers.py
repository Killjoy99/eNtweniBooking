import logging

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_async_db
from src.core.decorators import check_accept_header, render_template

from .models import Organisation
from .schemas import (
    OrganisationCreateSchema,
    OrganisationReadSchema,
    OrganisationDeactivateSchema,
    OrganisationUpdateSchema,
)
from .services import (
    get_all,
    get_by_id_filtered,
    get_or_create,
    update_organisation,
    set_organisation_status,
    delete_organisation,
)

logger = logging.getLogger(__name__)


organisation_router = APIRouter(prefix="/organisations", tags=["Organisation"])


@organisation_router.get("", name="organisations")
@render_template(template_name="organisation/list.html")
async def get_organisations(
    request: Request, 
    is_template: Optional[bool] = Depends(check_accept_header), 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Get all organisations."""
    organisations = await get_all(db_session=db_session)
    data = {"organisations": organisations}
    
    if is_template:
        return {"data": data, "error_message": None}
    
    return organisations

@organisation_router.post("")
async def create_organisation(
    organisation_in: OrganisationCreateSchema, 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Create a new organisation."""
    organisation = await get_or_create(db_session=db_session, organisation_in=organisation_in)
    return organisation

@organisation_router.get("/{organisation_id}", name="organisation_detail")
@render_template(template_name="organisation/detail.html")
async def get_organisation(
    request: Request, 
    organisation_id: int, 
    is_template: Optional[bool] = Depends(check_accept_header), 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Get an organisation by ID."""
    organisation = await get_by_id_filtered(db_session=db_session, id=organisation_id, active=True)
    
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    if is_template:
        return {"organisation": organisation, "error_message": None}
    
    return organisation

@organisation_router.put("/{organisation_id}", name="organisation_update")
@render_template(template_name="organisation/edit.html")
async def update(
    request: Request, 
    organisation_id: int, 
    organisation_in: OrganisationUpdateSchema, 
    is_template: Optional[bool] = Depends(check_accept_header), 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Update an organisation."""
    organisation = await update_organisation(db_session=db_session, organisation_id=organisation_id, organisation_in=organisation_in)
    
    if is_template:
        return {"organisation": organisation, "error_message": None}
    
    return organisation

@organisation_router.post("/{organisation_id}/deactivate", name="organisation_deactivate", response_model=OrganisationDeactivateSchema)
@render_template(template_name="organisation/detail.html")
async def deactivate_organisation(
    request: Request, 
    organisation_id: int, 
    is_template: Optional[bool] = Depends(check_accept_header), 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Deactivate an organisation."""
    organisation = await set_organisation_status(db_session=db_session, organisation_id=organisation_id, active=False)
    
    if is_template:
        RedirectResponse(request.url_for("organisations"), status_code=status.HTTP_302_FOUND)
        return {"organisation": organisation, "error_message": None}
    
    return organisation

@organisation_router.post("/{organisation_id}/reactivate", name="organisation_reactivate", response_model=OrganisationDeactivateSchema)
@render_template(template_name="organisation/detail.html")
async def reactivate_organisation(
    request: Request, 
    organisation_id: int, 
    is_template: Optional[bool] = Depends(check_accept_header), 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Reactivate an organisation."""
    organisation = await set_organisation_status(db_session=db_session, organisation_id=organisation_id, active=True)
    
    if is_template:
        return {"organisation": organisation, "error_message": None}
    
    return organisation

@organisation_router.delete("/{organisation_id}/delete", name="organisation_delete")
async def delete(
    request: Request, 
    organisation_id: int, 
    db_session: AsyncSession = Depends(get_async_db)
):
    """Delete an organisation."""
    try:
        await delete_organisation(db_session=db_session, organisation_id=organisation_id)
        return {"detail": f"Deleted Organisation with ID: {organisation_id}"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting organisation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
