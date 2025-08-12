from pydantic import BaseModel
from typing import Optional

# Schema for creating income range
class IncomeRangeCreate(BaseModel):
    description: str

# Schema for updating income range
class IncomeRangeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for income range output
class IncomeRangeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True