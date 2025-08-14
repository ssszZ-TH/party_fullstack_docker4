from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating contact mechanism type
class ContactMechanismTypeCreate(BaseModel):
    description: str

# Schema for updating contact mechanism type
class ContactMechanismTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for contact mechanism type output
class ContactMechanismTypeOut(BaseModel):
    id: int
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True