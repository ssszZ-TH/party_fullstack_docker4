from pydantic import BaseModel
from typing import Optional

# Schema for creating ethnicity type
class EthnicityTypeCreate(BaseModel):
    description: str

# Schema for updating ethnicity type
class EthnicityTypeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for ethnicity type output
class EthnicityTypeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True