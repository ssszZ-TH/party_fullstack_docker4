from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating relationship type
class RelationshipTypeCreate(BaseModel):
    description: str

# Schema for updating relationship type
class RelationshipTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for relationship type output
class RelationshipTypeOut(BaseModel):
    id: int
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True