from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List


class BusCreate(BaseModel):
    plate_number: str = Field(..., description="Plate number of the bus")
    route_ids: List[UUID] = Field(..., description="List of route IDs this bus will serve")


class BusOut(BaseModel):
    id: UUID
    plate_number: str
    created_at: datetime
    route_ids: List