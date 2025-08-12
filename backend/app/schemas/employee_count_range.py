from pydantic import BaseModel
from typing import Optional

# Schema for creating employee count range
class EmployeeCountRangeCreate(BaseModel):
    description: str

# Schema for updating employee count range
class EmployeeCountRangeUpdate(BaseModel):
    description: Optional[str] = None

# Schema for employee count range output
class EmployeeCountRangeOut(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True