from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from sqlalchemy.exc import IntegrityError

# from backend.auth.permissions import (
#     OrganisationOwnerPermission,
#     PermissionsDependency,
# )

# from backend.auth.service import CurrentUser
# from backend.database.core import DbSession
# from backend.database.service import CommonParamenters, search_filter_sort_paginate
from backend.enums import UserRoles
# from backend.exceptions import ExistsError
from backend.models import PrimaryKey

from .models import (
    OrganisationCreate,
    OrganizationRead,
    OrganisationUpdate,
    OrganizationPagination,
)
from .service import create, get, get_by_name, update, add_user


router = APIRouter()


@router.get("", response_model=OrganizationPagination)
async def get_organisations(common: CommonParamenters):
    """Get all aorganisations."""
    return search_filter_sort_paginate(model="Organisation", **common)


@router.post("", response_model=OrganizationRead)
async def create_organisation(db_session: DbSession, organisation_in: OrganisationCreate, current_user: CurrentUser,):
    """ Creates a new organisation"""
    organisation = get_by_name(db_session=db_session, name=organisation_in.name)
    if organisation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"message": "An organisation with this name already exists."}],
        )
    
    # create the Organisation
    organisation = create(db_session=db_session, organisation_in=organisation_in)
    
    # add the creator as the organisation owner
    add_user(db_session=db_session, organisation=organisation, user=current_user, role=UserRoles.owner)
    
    #TODO: Add other methods like a project, default post etc.
    
    return organisation


@router.get("/{organisation_id}", response_model=OrganizationRead)
async def get_organisation(db_session: DbSession, organisation_id: PrimaryKey):
    """ Get an organisation by id."""
    organisation = get(db_session=db_session, organisation_id=organisation_id)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"message": "An organisation with this id des not exist"}],
        )
    return organisation