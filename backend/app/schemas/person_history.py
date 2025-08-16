from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# Schema for person history output
class PersonHistoryOut(BaseModel):
    id: int
    person_id: Optional[int]
    username: Optional[str]
    password: Optional[str]
    personal_id_number: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    nick_name: Optional[str]
    birth_date: Optional[date]
    gender_type_id: Optional[int]
    marital_status_type_id: Optional[int]
    country_id: Optional[int]
    height: Optional[int]
    weight: Optional[int]
    ethnicity_type_id: Optional[int]
    income_range_id: Optional[int]
    comment: Optional[str]
    action: str
    action_at: datetime

    class Config:
        from_attributes = True