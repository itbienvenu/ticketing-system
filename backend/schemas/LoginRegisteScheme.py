from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timezone

class RegisterUser(BaseModel):
    # id: UUID = Field(default_factory=uuid4)
    full_name: str
    phone_number: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # updated_at: datetime =Field(default_factory=lambda: datetime.now(timezone.utc))



class LoginUser(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password_hash: str


class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None  # role name

class UserOut(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: Optional[str] = None