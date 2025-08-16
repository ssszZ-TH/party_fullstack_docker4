from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for communication event history output
class CommunicationEventHistoryOut(BaseModel):
    id: int
    communication_event_id: Optional[int]
    note: Optional[str]
    role_relationship_id: Optional[int]
    contact_mechanism_type_id: Optional[int]
    communication_event_status_type_id: Optional[int]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True