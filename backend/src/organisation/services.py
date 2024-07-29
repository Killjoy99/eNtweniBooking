from typing import List, Optional
from sqlalchemy.sql.expression import true
from sqlalchemy import select, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.enums import UserRoles

from .models import Organisation

from .schemas import (
    OrganisationCreateSchema,
    OrganisationReadSchema,
    OrganisationUpdateSchema,
)


async def get(*, db_session: AsyncSession, organisation_id: int) -> Organisation | None:
    """Gets an organisation by id"""
    query = select(Organisation).where(Organisation.id == organisation_id)
    result = await db_session.execute(query)
    organisation: Organisation = result.scalar_one_or_none()
    
    return organisation


async def get_default(*, db_session: AsyncSession) -> Organisation | None:
    """Gets the default organisation"""
    query = select(Organisation).where(Organisation.default == True)
    result = await db_session.execute(query)
    
    default_organisation: Organisation = result.scalar_one_or_none()
    
    return default_organisation


async def get_default_or_raise(*, db_session: AsyncSession) -> Organisation | str:
    """Returns the default organisation or raises an error if none exist"""
    default_organisation: Organisation = await get_default(db_session=db_session)
    
    if not default_organisation:
        raise ValidationError(
            [
                ErrorWrapper(
                    NotFoundError(msg="No default Organisation defined."), loc="organisation"
                )
            ],
            model=OrganisationRead,
        )
    return default_organisation


async def get_by_name(*, db_session: AsyncSession, name: str):
    """Gets an organisation by its name."""
    query = select(Organisation).where(Organisation.name == name)
    result = await db_session.execute(query)
    
    organisation: Organisation = result.scalar_one_or_none()
    
    return organisation


async def get_by_name_or_raise(*, db_session: AsyncSession, organisation_in=OrganisationReadSchema) -> Organisation:
    """ Returns the specified organisation or raises ValidationError"""
    organisation = await get_by_name(db_session=db_session, name=organisation_in.name)
    
    if not organisation:
        raise ValidationError(
            [
                ErrorWrapper(
                    NotFoundError(msg="Organisation not found.", organisation=organisation_in.name), loc="organisation"
                )
            ],
            model=OrganisationReadSchema,
        )
    return organisation


async def get_by_slug(*, db_session: AsyncSession, slug: str) -> Optional[Organisation]:
    """Gets an organisation by its slug."""
    query = select(Organisation).where(Organisation.slug == slug)
    result = await db_session.execute(query)
    
    organisation: Organisation = result.scalar_one_or_none()
    return organisation


async def get_by_slug_or_raise(*, db_session: AsyncSession, organisation_in=OrganisationReadSchema) -> Organisation:
    """ Returns the organisation specified or raises ValidationError"""
    organisation = await get_by_slug(db_session=db_session, slug=organisation_in.slug)
    
    if not organisation:
        raise ValidationError(
            [
                ErrorWrapper(
                    NotFoundError(msg="Organisation not found", organisation=organisation_in.name), loc="organisation"
                )
            ],
            model=OrganisationRead,
        )
    return organisation


async def get_by_name_or_default(*, db_session: AsyncSession, organisation_in=OrganisationReadSchema) -> Organisation:
    """ Returns an organisation based on a name or default if not specified."""
    if organisation_in.name:
        return await get_by_name_or_raise(db_session=db_session, organisation_in=organisation_in)
    else:
        return await get_default_or_raise(db_session=db_session)
    

async def get_all(*, db_session: AsyncSession) -> List[Organisation] | None:
    """ Gets all organisations"""
    query = select(Organisation).where(and_(Organisation.active == True, Organisation.is_deleted == False))
    result = await db_session.execute(query)
    
    organisations: List[Organisation] = result.scalars()
    
    return organisations


async def create(*, db_session: AsyncSession, organisation_in=OrganisationCreateSchema) -> Organisation:
    """ Creates an organisation"""
    organisation = Organisation(
        **organisation_in.dict(exclude={"banner_color"}),
    )
    
    if organisation_in.banner_color:
        organisation.banner_color = organisation_in.banner_color.as_hex()
        
    # let the new schema session create the Organisation
    organisation = init_schema(engine=engine, organisation=organisation)
    return organisation


async def get_or_create(*, db_session: AsyncSession, organisation_in=OrganisationCreateSchema) -> Organisation:
    """ Gets an existing or creates a new organisation."""
    if organisation_in.id:
        q = db_session.query(Organisation).filter(Organisation.id == organisation_in.id)
    else:
        q = db_session.query(Organisation).filter_by(**organisation_in.dict(exclude={"id"}))
        
    instance = q.first()
    if instance:
        return instance
    
    return create(db_session=db_session, organisation_in=organisation_in)


async def update(*, db_session: AsyncSession, organisation=Organisation, organisation_in=OrganisationUpdateSchema) -> Organisation:
    """Updates an organisation."""
    organisation_data = organisation.dict()
    update_data = organisation_in.dict(exclude_defaults=True, exclude={"banner_color"})
    
    for field in organisation_data:
        if field in update_data:
            setattr(organisation, field, update_data[field])
            
    if organisation_in.banner_color:
        organisation.banner_color = organisation_in.banner_color.as_hex()
        
    db_session.commit()
    return organisation


async def delete(*, db_session: AsyncSession, organisation_id: int):
    """Deletes an organisation"""
    organisation = db_session.query(Organisation).filter(Organisation.id == organisation_id).first()
    db_session.delete(organisation)
    db_session.commit()
    

# async def add_user(*, db_session: AsyncSession, user: EntweniBookingUser, organisation: Organisation, role: UserRoles = UserRoles.member):
#     """Adds a user to an organisation"""
#     db_session.add(
#         EntweniBookingUserOrganisation(
#             entwenibooking_user_id=user.id, organisation_id=organisation.id, role=role
#         )
#     )
#     db_session.commit()