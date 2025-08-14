from pydantic import BaseModel
from typing import Optional

# Schema for creating communication event purpose type
class CommunicationEventPurposeTypeCreate(BaseModel):
    description: str

# Schema for updating communication event purpose type
class CommunicationEventPurposeTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for communication event purpose type output
class CommunicationEventPurposeTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True