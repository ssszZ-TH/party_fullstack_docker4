from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for organization history output
class OrganizationHistoryOut(BaseModel):
    id: int
    organization_id: Optional[int]
    federal_tax_id: Optional[str]
    name_en: Optional[str]
    name_th: Optional[str]
    organization_type_id: Optional[int]
    industry_type_id: Optional[int]
    employee_count_range_id: Optional[int]
    username: Optional[str]
    password: Optional[str]
    comment: Optional[str]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True
        