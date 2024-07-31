import logging
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from .models import Organisation
from .schemas import OrganisationCreateSchema, OrganisationReadSchema, OrganisationUpdateSchema

logger = logging.getLogger(__name__)

async def get_default(*, db_session: AsyncSession) -> Organisation | None:
    """Gets the default organisation."""
    query = select(Organisation).where(Organisation.default.is_(True))
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

async def filter_active_and_not_deleted(query):
    """Filters organisations that are active and not deleted."""
    return query.where(and_(Organisation.active.is_(True), Organisation.is_deleted.is_(False)))

async def get_default_or_raise(*, db_session: AsyncSession) -> Organisation:
    """Returns the default organisation or raises an HTTPException if none exist."""
    default_organisation = await get_default(db_session=db_session)
    if default_organisation is None:
        raise HTTPException(status_code=404, detail="Default organisation not found")
    return default_organisation

async def get_by_id_filtered(*, db_session: AsyncSession, id: int, active: Optional[bool] = None) -> Organisation | None:
    """Gets an organisation by its ID with optional active status filter."""
    query = select(Organisation).where(Organisation.id == id)
    if active is not None:
        query = query.where(Organisation.active.is_(active))
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

async def get_by_attribute(*, db_session: AsyncSession, attribute_name: str, attribute_value: str) -> Organisation | None:
    """Gets an organisation by a given attribute."""
    query = select(Organisation).where(getattr(Organisation, attribute_name) == attribute_value)
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

async def get_by_name_or_raise(*, db_session: AsyncSession, organisation_in: OrganisationReadSchema) -> Organisation:
    """Returns the specified organisation or raises HTTPException."""
    organisation = await get_by_attribute(db_session=db_session, attribute_name="name", attribute_value=organisation_in.name)
    if organisation is None:
        raise HTTPException(status_code=404, detail=f"Organisation with name '{organisation_in.name}' not found")
    return organisation

async def get_by_slug_or_raise(*, db_session: AsyncSession, organisation_in: OrganisationReadSchema) -> Organisation:
    """Returns the organisation specified or raises HTTPException."""
    organisation = await get_by_attribute(db_session=db_session, attribute_name="slug", attribute_value=organisation_in.slug)
    if organisation is None:
        raise HTTPException(status_code=404, detail=f"Organisation with slug '{organisation_in.slug}' not found")
    return organisation

async def get_or_default(*, db_session: AsyncSession, name: Optional[str] = None) -> Organisation:
    """Returns an organisation by name or default if not specified."""
    if name:
        organisation = await get_by_attribute(db_session=db_session, attribute_name='name', attribute_value=name)
        if organisation:
            return organisation
    return await get_default_or_raise(db_session=db_session)

async def get_all(*, db_session: AsyncSession) -> List[Organisation] | None:
    """Gets all organisations."""
    query = select(Organisation)
    query = await filter_active_and_not_deleted(query)  # Apply filter here
    result = await db_session.execute(query)
    return result.scalars().all()

async def get_or_create(*, db_session: AsyncSession, organisation_in: OrganisationCreateSchema) -> Organisation:
    """Gets an existing organisation or creates a new one."""
    organisation = await get_by_attribute(db_session=db_session, attribute_name='name', attribute_value=organisation_in.name)
    if organisation is None:
        try:
            organisation = Organisation(**organisation_in.dict())
            db_session.add(organisation)
            await db_session.commit()
            await db_session.refresh(organisation)
        except SQLAlchemyError as e:
            logger.error(f"Error creating organisation: {e}")
            await db_session.rollback()
            raise HTTPException(status_code=500, detail="Failed to create organisation")
    return organisation

async def update_organisation(*, db_session: AsyncSession, organisation_id: int, organisation_in: OrganisationUpdateSchema) -> Organisation:
    """Updates an organisation."""
    organisation = await get_by_id_filtered(db_session=db_session, id=organisation_id, active=True)
    if organisation is None:
        raise HTTPException(status_code=404, detail="Organisation not found")

    for field, value in organisation_in.model_dump(exclude_unset=True).items():
        setattr(organisation, field, value)
    
    db_session.add(organisation)
    await db_session.commit()
    await db_session.refresh(organisation)
    
    return organisation

async def set_organisation_status(*, db_session: AsyncSession, organisation_id: int, active: bool) -> Organisation | None:
    """Sets the active status of an organisation."""
    organisation = await get_by_id_filtered(db_session=db_session, id=organisation_id)
    if organisation is None:
        raise HTTPException(status_code=404, detail="Organisation not found")

    organisation.active = active
    db_session.add(organisation)
    await db_session.commit()
    await db_session.refresh(organisation)
    
    return organisation

async def delete_organisation(*, db_session: AsyncSession, organisation_id: int):
    """Deletes an organisation."""
    organisation = await get_by_id_filtered(db_session=db_session, id=organisation_id)
    if organisation is None or organisation.is_deleted:
        raise HTTPException(status_code=404, detail="Organisation not found or already deleted")

    organisation.is_deleted = True
    db_session.add(organisation)
    await db_session.commit()
