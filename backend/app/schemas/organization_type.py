from pydantic import BaseModel
from typing import Optional

# Schema for creating organization type
class OrganizationTypeCreate(BaseModel):
    description: str

# Schema for updating organization type
class OrganizationTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for organization type output
class OrganizationTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True