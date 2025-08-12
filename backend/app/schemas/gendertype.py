from pydantic import BaseModel
from typing import Optional

# Schema for creating gender type
class GenderTypeCreate(BaseModel):
    description: str

# Schema for updating gender type
class GenderTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for gender type output
class GenderTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True