from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating role type
class RoleTypeCreate(BaseModel):
    description: str

# Schema for updating role type
class RoleTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for role type output
class RoleTypeOut(BaseModel):
    id: int
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True