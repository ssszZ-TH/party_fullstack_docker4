from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating priority type
class PriorityTypeCreate(BaseModel):
    description: str

# Schema for updating priority type
class PriorityTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for priority type output
class PriorityTypeOut(BaseModel):
    id: int
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True