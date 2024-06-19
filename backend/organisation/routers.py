from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from database.core import get_db
from organisation.models import Organisation
from organisation.schemas import OrganisationCreate, OrganisationRead

from core.decorators import check_accept_header, render_template, return_json


organisation_router = APIRouter()


@organisation_router.get("")
async def get_organisations(request: Request, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession] = Depends(get_db)):
    """Get all aorganisations."""
    statement = await db.execute(select(Organisation))
    organisations = statement.scalars().all()
    data = {"organisations": organisations}
    
    if is_template:
        return render_template(request=request, template_name="organisation/list.html", context=data)
    else:
        return organisations


@organisation_router.post("")
async def create_organisation(request: Request, organisation: OrganisationCreate, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    organisation_to_db = Organisation(**organisation.dict())
    db.add(organisation_to_db)
    await db.commit()
    await db.refresh(organisation_to_db)
    return organisation_to_db


@organisation_router.get("/{organisation_id}", name="organisation")
async def get_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    """ Get an organisation by id."""
    statement = await db.execute(select(Organisation).where(Organisation.id==organisation_id))
    organisation = statement.scalar()
    
    if is_template:
        return render_template(request=request, template_name="organisation/detail.html", context=organisation)
    return organisation


@organisation_router.put("/{organisation_id}")
async def update_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Updated Organisation with ID: {organisation_id}"}


@organisation_router.delete("/{organisation_id}")
async def delete_organisation(request: Request, organisation_id: int, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Deleted Organisation with ID:{organisation_id}"}