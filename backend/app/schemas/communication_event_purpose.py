from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a communication event purpose
class CommunicationEventPurposeCreate(BaseModel):
    note: Optional[str] = None
    communication_event_id: Optional[int] = None
    communication_event_purpose_type_id: Optional[int] = None

# Schema for updating a communication event purpose
class CommunicationEventPurposeUpdate(BaseModel):
    note: Optional[str] = None
    communication_event_id: Optional[int] = None
    communication_event_purpose_type_id: Optional[int] = None

# Schema for communication event purpose output
class CommunicationEventPurposeOut(BaseModel):
    id: int
    note: Optional[str]
    communication_event_id: Optional[int]
    communication_event_purpose_type_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True