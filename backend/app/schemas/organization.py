from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating organization
class OrganizationCreate(BaseModel):
    federal_tax_id: Optional[str] = None
    name_en: str
    name_th: Optional[str] = None
    organization_type_id: int
    username: str
    password: str

# Schema for updating organization
class OrganizationUpdate(BaseModel):
    federal_tax_id: Optional[str] = None
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    organization_type_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None

# Schema for organization output
class OrganizationOut(BaseModel):
    id: int
    federal_tax_id: Optional[str] = None
    name_en: str
    name_th: Optional[str] = None
    organization_type_id: int
    username: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schema for organization login
class OrganizationLogin(BaseModel):
    username: str
    password: str