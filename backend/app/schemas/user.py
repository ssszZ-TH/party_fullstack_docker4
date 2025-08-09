from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema for creating user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = None

# Schema for updating user
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Schema for user output
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str