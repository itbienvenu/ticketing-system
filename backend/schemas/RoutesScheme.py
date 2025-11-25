from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone


class RegisterRoute(BaseModel):
    origin_id: UUID  # store ID, not name
    destination_id: UUID  # store ID, not name
    # price: int
    # company_id: Optional[UUID] = None


class RouteOut(BaseModel):
    id: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    company_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True # allows SQLAlchemy object -> Pydantic
        

class UpdateRoute(BaseModel):
    origin_id: Optional[UUID] = None
    destination_id: Optional[UUID] = None
    price: Optional[float] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssignBusRequest(BaseModel):
    route_id: UUID
    bus_id: UUID
