from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a party role
class PartyRoleCreate(BaseModel):
    note: Optional[str] = None
    role_type_id: Optional[int] = None

# Schema for updating a party role
class PartyRoleUpdate(BaseModel):
    note: Optional[str] = None
    role_type_id: Optional[int] = None

# Schema for party role output
class PartyRoleOut(BaseModel):
    id: int
    note: Optional[str]
    party_id: Optional[int]
    role_type_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True