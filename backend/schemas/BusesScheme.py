from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class BusCreate(BaseModel):
    plate_number: str = Field(..., description="Plate number of the bus")
    capacity: int = Field(..., description="Seats for a certain bus")
    route_ids: List[UUID] = Field(default=None, description="List of route IDs this bus will serve")


class BusOut(BaseModel):
    id: UUID
    plate_number: str
    capacity: int
    available_seats: int
    created_at: datetime
    route_ids: List

class UpdateBus(BaseModel):
    plate_number: Optional[str] = None
    capacity: Optional[int] = None
    route_ids: Optional[List] = None  