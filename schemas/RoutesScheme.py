from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta, UTC


class RegisterRoute(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    origin: str
    destination: str
    price: int
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    
class RouteOut(BaseModel):
    id: UUID
    origin: str
    destination: str
    price: float

class UpdateRoute(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    price: Optional[float] = None
    updated_at: datetime = datetime.now(UTC)
