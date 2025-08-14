from pydantic import BaseModel
from typing import Optional

# Schema for creating communication event status type
class CommunicationEventStatusTypeCreate(BaseModel):
    description: str

# Schema for updating communication event status type
class CommunicationEventStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for communication event status type output
class CommunicationEventStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True