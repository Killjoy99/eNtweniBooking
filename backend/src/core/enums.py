from enum import Enum


class EntweniBookingEnum(Enum):
    def __str__(self) -> str:
        return str.__str__(self.name)
    
    
class Visibility(EntweniBookingEnum):
    open = "Open"
    restricted = "Restricted"
    

class SearchTypes(EntweniBookingEnum):
    hotel = "Hotel"
    plugin = "Plugin"
    search_filter = "SearchFilter"
    query = "Query"
    service = "Service"
    individual_contact = "IndividualContact"
    
    
class UserRoles(EntweniBookingEnum):
    owner = "Owner"
    manager = "Manager"
    admin = "Admin"
    member = "Member"
    

class AccountType(Enum):
    SUPERUSER = 'super_user'
    AGENT = 'agent'
    CUSTOMER = 'customer'
    ORGANISATION = "organisation"