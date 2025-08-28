from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta, UTC


class RegisterRoute(BaseModel):
    origin: str
    destination: str
    price: int
    # created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    
class RouteOut(BaseModel):
    price: int
    id: UUID
    origin: str
    destination: str
    created_at: datetime

    class Config:
        from_attributes = True

class UpdateRoute(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    price: Optional[float] = None
    updated_at: datetime = datetime.now(UTC)
