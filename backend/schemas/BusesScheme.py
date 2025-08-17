from pydantic import BaseModel, Field
from uuid import UUID

class BusCreate(BaseModel):
    id: UUID
    plate_number: str = Field(..., description="Plate number of the bus")

