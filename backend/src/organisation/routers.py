from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from src.database.core import get_async_db
from src.core.decorators import check_accept_header, render_template, return_json

from .models import Organisation
from .schemas import OrganisationCreateSchema, OrganisationReadSchema, OrganisationDeactivateSchema
from .services import get_all, get_by_id, deactivate, create


organisation_router = APIRouter()


@organisation_router.get("")
async def get_organisations(request: Request, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession] = Depends(get_async_db)):
    """Get all aorganisations."""
    organisations: OrganisationResponseSchema = await get_all(db_session=db_session)
    
    data = {"organisations": organisations}
    
    if is_template:
        return render_template(request=request, template_name="organisation/list.html", context=data)
    
    return organisations


@organisation_router.post("")
async def create_organisation(request: Request, organisation_in: OrganisationCreateSchema, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
    
    organisation: Organisation = await create(db_session=db_session, organisation_in=organisation_in)
    
    
    # db.add(organisation_to_db)
    # await db.commit()
    # await db.refresh(organisation_to_db)
    return organisation


@organisation_router.get("/{organisation_id}", name="organisation")
async def get_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
    """ Get an organisation by id."""
    
    organisation: Organisation = await get_by_id(db_session=db_session, id=organisation_id)
    
    if is_template:
        return render_template(request=request, template_name="organisation/detail.html", context={"organisation": organisation})
    return organisation


@organisation_router.put("/{organisation_id}", name="organisation_update")
async def update_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
    return {"detail": f"Updated Organisation with ID: {organisation_id}"}


@organisation_router.post("/{organisation_id}", name="organisation_deactivate", response_model=OrganisationDeactivateSchema)
async def deactivate_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
    """ Deactivate an organisation based on its ID"""
    
    organisation: Organisation = await deactivate(db_session=db_session, organisation_id=organisation_id)
    
    if is_template:
        return render_template(request=request, template_name="organisation/detail.html", context={"organisation": organisation})
    return organisation


@organisation_router.delete("/{organisation_id}", name="organisation_delete")
async def delete_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession]=Depends(get_async_db)):
    return {"detail": f"Deleted Organisation with ID:{organisation_id}"}