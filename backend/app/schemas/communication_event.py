from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a communication event
class CommunicationEventCreate(BaseModel):
    note: Optional[str] = None
    role_relationship_id: Optional[int] = None
    contact_mechanism_type_id: Optional[int] = None
    communication_event_status_type_id: Optional[int] = None

# Schema for updating a communication event
class CommunicationEventUpdate(BaseModel):
    note: Optional[str] = None
    role_relationship_id: Optional[int] = None
    contact_mechanism_type_id: Optional[int] = None
    communication_event_status_type_id: Optional[int] = None

# Schema for communication event output
class CommunicationEventOut(BaseModel):
    id: int
    note: Optional[str]
    role_relationship_id: Optional[int]
    contact_mechanism_type_id: Optional[int]
    communication_event_status_type_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True