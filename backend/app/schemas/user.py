from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BasetypeAdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str