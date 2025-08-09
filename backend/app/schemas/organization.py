from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizationCreate(BaseModel):
    federal_tax_id: Optional[str] = None
    name_en: str
    name_th: Optional[str] = None
    organization_type_id: int

class OrganizationUpdate(BaseModel):
    federal_federal_tax_id: Optional[str] = None
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    organization_type_id: Optional[int] = None

class OrganizationOut(BaseModel):
    id: int
    federal_tax_id: Optional[str] = None
    name_en: str
    name_th: Optional[str] = None
    organization_type_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True