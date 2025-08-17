from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class BusCreate(BaseModel):
    id: UUID
    plate_number: str = Field(..., description="Plate number of the bus")


class BusOut(BaseModel):
    id: UUID
    plate_number: str
    created_at: datetime