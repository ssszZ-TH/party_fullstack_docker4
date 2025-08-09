from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PersonCreate(BaseModel):
    username: str
    password: str
    personal_id_number: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    nick_name: Optional[str] = None
    birth_date: date
    gender_type_id: int
    marital_status_type_id: int
    country_id: int
    height: int
    weight: int
    ethnicity_type_id: int
    income_range_id: int
    comment: Optional[str] = None

class PersonUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    personal_id_number: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    nick_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender_type_id: Optional[int] = None
    marital_status_type_id: Optional[int] = None
    country_id: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    ethnicity_type_id: Optional[int] = None
    income_range_id: Optional[int] = None
    comment: Optional[str] = None

class PersonOut(BaseModel):
    id: int
    username: str
    personal_id_number: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    nick_name: Optional[str] = None
    birth_date: date
    gender_type_id: int
    marital_status_type_id: int
    country_id: int
    height: int
    weight: int
    ethnicity_type_id: int
    income_range_id: int
    comment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True