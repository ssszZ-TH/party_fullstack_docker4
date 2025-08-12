from pydantic import BaseModel
from typing import Optional

# Schema for creating country
class CountryCreate(BaseModel):
    iso_code: str
    name_en: str
    name_th: Optional[str] = None

# Schema for updating country
class CountryUpdate(BaseModel):
    iso_code: Optional[str] = None
    name_en: Optional[str] = None
    name_th: Optional[str] = None

# Schema for country output
class CountryOut(BaseModel):
    id: int
    iso_code: str
    name_en: str
    name_th: Optional[str] = None

    class Config:
        from_attributes = True