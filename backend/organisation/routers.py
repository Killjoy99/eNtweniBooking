from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from database.core import get_db
from organisation.models import Organisation
from organisation.schemas import OrganisationCreate, OrganisationRead


organisation_router = APIRouter()


@organisation_router.get("")
async def get_organisations(db: async_sessionmaker[AsyncSession] = Depends(get_db)):
    """Get all aorganisations."""
    statement = await db.execute(select(Organisation))
    organisations = statement.scalars().all()
    return {"organisations": organisations}


@organisation_router.post("")
async def create_organisation(organisation: OrganisationCreate, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    organisation_to_db = Organisation(**organisation.dict())
    db.add(organisation_to_db)
    await db.commit()
    await db.refresh(organisation_to_db)
    return organisation_to_db
    # return {"detail": f"Created an Organisation: {organisation_to_db}"}
    # return organisation_to_db


@organisation_router.get("/{organisation_id}")
async def get_organisation(organisation_id: int, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    """ Get an organisation by id."""
    return {"detail": f"Got Organisation with ID {organisation_id}"}


@organisation_router.put("/{organisation_id}")
async def update_organisation(organisation_id: int, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Updated Organisation with ID: {organisation_id}"}


@organisation_router.delete("/{organisation_id}")
async def delete_organisation(organisation_id: int, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Deleted Organisation with ID:{organisation_id}"}