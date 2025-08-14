from pydantic import BaseModel
from typing import Optional
from datetime import date

# Schema for creating a passport
class PassportCreate(BaseModel):
    passport_id_number: str
    issue_date: date
    expire_date: date
    person_id: int

# Schema for updating a passport
class PassportUpdate(BaseModel):
    passport_id_number: Optional[str] = None
    issue_date: Optional[date] = None
    expire_date: Optional[date] = None
    person_id: Optional[int] = None

# Schema for passport output
class PassportOut(BaseModel):
    id: int
    passport_id_number: str
    issue_date: date
    expire_date: date
    person_id: Optional[int]
    created_at: date
    updated_at: Optional[date]

    class Config:
        from_attributes = True