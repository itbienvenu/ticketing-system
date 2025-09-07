from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone


class RegisterRoute(BaseModel):
    origin_id: UUID  # store ID, not name
    destination_id: UUID  # store ID, not name
    price: int
    company_id: Optional[UUID] = None


class RouteOut(BaseModel):
    id: UUID
    price: int
    origin: str  # return station name
    destination: str  # return station name
    created_at: datetime

    class Config:
        orm_mode = True  # allows SQLAlchemy object -> Pydantic
        

class UpdateRoute(BaseModel):
    origin_id: Optional[UUID] = None
    destination_id: Optional[UUID] = None
    price: Optional[float] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssignBusRequest(BaseModel):
    route_id: UUID
    bus_id: UUID
