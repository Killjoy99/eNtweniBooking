from enum import Enum


class EntweniBookingEnum(Enum):
    def __str__(self) -> str:
        return str.__str__(self)
    
    
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
    
    
class EventType(EntweniBookingEnum):
    other = "Other"  # default and catch-all (x resource created/updated, etc.)
    field_updated = "Field updated"  # for fields like title, description, tags, type, etc.
    assessment_updated = "Assessment updated"  # for priority, status, or severity changes
    participant_updated = "Participant updated"  # for added/removed users and role changes
    imported_message = "Imported message"  # for stopwatch-reacted messages from Slack
    custom_event = "Custom event"  # for user-added events (new feature)