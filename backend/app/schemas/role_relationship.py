from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a role relationship
class RoleRelationshipCreate(BaseModel):
    to_party_role_id: int
    comment: Optional[str] = None
    relationship_type_id: int
    priority_type_id: Optional[int] = None
    role_relationship_status_type_id: Optional[int] = None

# Schema for updating a role relationship
class RoleRelationshipUpdate(BaseModel):
    to_party_role_id: Optional[int] = None
    comment: Optional[str] = None
    relationship_type_id: Optional[int] = None
    priority_type_id: Optional[int] = None
    role_relationship_status_type_id: Optional[int] = None

# Schema for role relationship output
class RoleRelationshipOut(BaseModel):
    id: int
    from_party_role_id: Optional[int]
    to_party_role_id: Optional[int]
    comment: Optional[str]
    relationship_type_id: Optional[int]
    priority_type_id: Optional[int]
    role_relationship_status_type_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True