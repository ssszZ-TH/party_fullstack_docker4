from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# Schema for passport history output
class PassportHistoryOut(BaseModel):
    id: int
    passport_id: Optional[int]
    passport_id_number: Optional[str]
    issue_date: Optional[date]
    expire_date: Optional[date]
    person_id: Optional[int]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True