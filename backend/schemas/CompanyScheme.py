from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    full_name: str
    email: str
    phone_number: str
    password: str
    
class PasswordChange(BaseModel):
    old_password: str
    new_password: str