from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class TicketCreate(BaseModel):
    user_id: UUID = Field(..., description="ID of the user booking the ticket")
    bus_id: UUID = Field(..., description="ID of the bus")
    route_id: UUID = Field(..., description="ID of the route")

class TicketResponse(BaseModel):
    id: UUID
    user_id: UUID
    qr_code: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  