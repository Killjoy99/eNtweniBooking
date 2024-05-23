from typing import List, Optional
from sqlalchemy.sql.expression import true
# from pydantic.error_wrappers import ErrorWrapper, ValidationError

# from backend.auth.models import EntweniBookingUser, EntweniBookingUserOrganisation
# from backend.database.core import engine
# from backend.database.manager import init_schema
from backend.enums import UserRoles
# from backend.exceptions import NotFoundError

from .models import Organisation, OrganisationCreate, OrganizationRead, OrganisationUpdate


def get(*, db_session, organisation_id: int) -> Optional[Organisation]:
    """Gets an organisation by id"""
    return db_session.query(Organisation).filter(Organisation.id == organisation_id).first()


def get_default(*, db_session) -> Optional[Organisation]:
    """Gets the default organisation"""
    return db_session.query(Organisation).filter(Organisation.default == true()).one_or_none()


def get_default_or_raise(*, db_session) -> Organisation:
    """Returns the default organisation or raises an error if none exist"""
    organisation = get_default(db_session=db_session)
    
    if not organisation:
        raise ValidationError(
            [
                ErrorWrapper(
                    NotFoundError(msg="No default Organisation defined."), loc="organisation"
                )
            ],
            model=OrganisationRead,
        )
    return organisation


def get_by_name(*, db_session, name: str):
    """Gets an organisation by its name."""
    return db_session.query(Organisation).filter(Organisation.name == name).one_or_none()


def get_by_name_or_raise(*, db_session, organisation_in=OrganizationRead) -> Organisation:
    """ Returns the specified organisation or raises ValidationError"""
    organisation = get_by_name(db_session=db_session, name=organisation_in.name)
    
    if not organisation:
        raise ValidationError(
            [
                ErrorWrapper(
                    NotFoundError(msg="Organisation not found.", organisation=organisation_in.name), loc="organisation"
                )
            ],
            model=OrganizationRead,
        )
    return organisation


def get_by_slug(*, db_session, slug: str) -> Optional[Organisation]:
    """Gets an organisation by its slug."""
    return db_session.query(Organisation).filter(Organisation.slug == slug).one_or_none()


def get_by_slug_or_raise(*, db_session, organisation_in=OrganizationRead) -> Organization:
    """ Returns the organisation specified or raises ValidationError"""
    organisation = get_by_slug(db_session=db_session, slug=organisation_in.slug)
    
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


def get_by_name_or_default(*, db_session, organisation_in=OrganizationRead) -> Organisation:
    """ Returns an organisation based on a name or default if not specified."""
    if organisation_in.name:
        return get_by_name_or_raise(db_session=db_session, organisation_in=organisation_in)
    else:
        return get_default_or_raise(db_session=db_session)
    

def get_all(*, db_session) -> List[Optional[Organisation]]:
    """ Gets all organisations"""
    return db_session.query(Organisation)


def create(*, db_session, organisation_in=OrganisationCreate) -> Organisation:
    """ Creates an organisation"""
    organisation = Organisation(
        **organisation_in.dict(exclude={"banner_color"}),
    )
    
    if organisation_in.banner_color:
        organisation.banner_color = organisation_in.banner_color.as_hex()
        
    # let the new schema session create the Organisation
    organisation = init_schema(engine=engine, organisation=organisation)
    return organisation


def get_or_create(*, db_session, organisation_in=OrganisationCreate) -> Organisation:
    """ Gets an existing or creates a new organisation."""
    if organisation_in.id:
        q = db_session.query(Organisation).filter(Organisation.id == organisation_in.id)
    else:
        q = db_session.query(Organisation).filter_by(**organisation_in.dict(exclude={"id"}))
        
    instance = q.first()
    if instance:
        return instance
    
    return create(db_session=db_session, organisation_in=organisation_in)


def update(*, db_session, organisation=Organisation, organisation_in=OrganisationUpdate) -> Organisation:
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


def delete(*, db_session, organisation_id: int):
    """Deletes an organisation"""
    organisation = db_session.query(Organisation).filter(Organisation.id == organisation_id).first()
    db_session.delete(organisation)
    db_session.commit()
    

def add_user(*, db_session, user: EntweniBookingUser, organisation: Organisation, role: UserRoles = UserRoles.member):
    """Adds a user to an organisation"""
    db_session.add(
        EntweniBookingUserOrganisation(
            entwenibooking_user_id=user.id, organisation_id=organisation.id, role=role
        )
    )
    db_session.commit()