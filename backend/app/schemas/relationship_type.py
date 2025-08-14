from pydantic import BaseModel
from typing import Optional

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

    class Config:
        from_attributes = True