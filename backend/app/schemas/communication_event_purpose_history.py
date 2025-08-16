from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for communication event purpose history output
class CommunicationEventPurposeHistoryOut(BaseModel):
    id: int
    communication_event_purpose_id: Optional[int]
    note: Optional[str]
    communication_event_id: Optional[int]
    communication_event_purpose_type_id: Optional[int]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True