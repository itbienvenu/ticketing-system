from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, UTC, timezone

class Register(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    full_name: str
    phone_number: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime =Field(default_factory=lambda: datetime.now(timezone.utc))

class Login(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str