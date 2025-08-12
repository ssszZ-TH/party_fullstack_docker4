from pydantic import BaseModel
from typing import Optional

# Schema for creating marital status type
class MaritalStatusTypeCreate(BaseModel):
    description: str

# Schema for updating marital status type
class MaritalStatusTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for marital status type output
class MaritalStatusTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True