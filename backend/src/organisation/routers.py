from re import template
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from src.database.core import get_async_db
from src.core.decorators import check_accept_header, render_template, return_json

from .models import Organisation
from .schemas import OrganisationCreateSchema, OrganisationReadSchema, OrganisationDeactivateSchema, OrganisationUpdateSchema, OrganisationResponseSchema
from .services import (
    get_all,
    get_by_id_filtered,
    get_or_create,
    update_organisation,
    set_organisation_status,
    delete_organisation,
    )

organisation_router = APIRouter(prefix="/organisations", tags=["Organisation"])


@organisation_router.get("")
@render_template(template_name="organisation/list.html")
async def get_organisations(request: Request, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession = Depends(get_async_db)):
    """Get all aorganisations."""
    organisations = await get_all(db_session=db_session)
    
    data = {"organisations": organisations}
    
    if is_template:
        return {"data": data, "error_message": None}
    
    return organisations


@organisation_router.post("")
async def create_organisation(request: Request, organisation_in: OrganisationCreateSchema, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession=Depends(get_async_db)):
    
    organisation: Organisation = await get_or_create(db_session=db_session, organisation_in=organisation_in)

    return organisation


@organisation_router.get("/{organisation_id}", name="organisation")
@render_template(template_name="organisation/detail.html")
async def get_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession=Depends(get_async_db)):
    """ Get an organisation by id."""
    
    organisation = await get_by_id_filtered(db_session=db_session, id=organisation_id, active=True)
    
    if is_template:
        return {"organisation": organisation, "error_message": None}
    return organisation


@organisation_router.put("/{organisation_id}", name="organisation_update")
@render_template(template_name="organisation/edit.html")
async def update(request: Request, organisation_in: OrganisationUpdateSchema, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession=Depends(get_async_db)):
    
    organisation = await update_organisation(db_session=db_session, organisation_in=organisation_in)

    if is_template:
        return {"organisation": organisation, "error_message": None}
    return organisation
    
    


@organisation_router.post("/{organisation_id}", name="organisation_deactivate", response_model=OrganisationDeactivateSchema)
@render_template(template_name="organisation/detail.html")
async def deactivate(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession=Depends(get_async_db)):
    """ Deactivate an organisation based on its ID"""
    
    organisation = await set_organisation_status(db_session=db_session, organisation_id=organisation_id, active=False)
    
    if is_template:
        return {"organisation": organisation, "error_message": None}
    return organisation

@organisation_router.post("/{organisation_id}", name="organisation_reactivate", response_model=OrganisationDeactivateSchema)
@render_template(template_name="organisation/detail.html")
async def reactivate(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession=Depends(get_async_db)):
    """ Deactivate an organisation based on its ID"""
    
    organisation = await set_organisation_status(db_session=db_session, organisation_id=organisation_id, active=True)
    
    if is_template:
        return {"organisation": organisation, "error_message": None}
    return organisation


@organisation_router.delete("/{organisation_id}", name="organisation_delete")
async def delete(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: AsyncSession=Depends(get_async_db)):
    try:
        await delete_organisation(request=request, organisation_id=organisation_id)
        return {"detail": f"Deleted Organisation with ID:{organisation_id}"}
    except:
        return {"detail": f"Could not find Organisation with ID:{organisation_id}"}