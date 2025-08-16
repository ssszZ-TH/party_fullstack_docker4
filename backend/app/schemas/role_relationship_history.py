from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for role relationship history output
class RoleRelationshipHistoryOut(BaseModel):
    id: int
    role_relationship_id: Optional[int]
    from_party_role_id: Optional[int]
    to_party_role_id: Optional[int]
    comment: Optional[str]
    relationship_type_id: Optional[int]
    priority_type_id: Optional[int]
    role_relationship_status_type_id: Optional[int]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True