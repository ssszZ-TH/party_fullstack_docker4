from pydantic import BaseModel
from typing import Optional

# Schema for creating role relationship status type
class RoleRelationshipStatusTypeCreate(BaseModel):
    description: str

# Schema for updating role relationship status type
class RoleRelationshipStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for role relationship status type output
class RoleRelationshipStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True