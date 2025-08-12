from pydantic import BaseModel
from typing import Optional

# Schema for creating industry type
class IndustryTypeCreate(BaseModel):
    naisc: str
    description: str

# Schema for updating industry type
class IndustryTypeUpdate(BaseModel):
    naisc: Optional[str] = None
    description: Optional[str] = None

# Schema for industry type output
class IndustryTypeOut(BaseModel):
    id: int
    naisc: str
    description: str

    class Config:
        from_attributes = True