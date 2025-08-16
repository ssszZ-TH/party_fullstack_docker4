from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for party role history output
class PartyRoleHistoryOut(BaseModel):
    id: int
    party_role_id: Optional[int]
    note: Optional[str]
    party_id: Optional[int]
    role_type_id: Optional[int]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True