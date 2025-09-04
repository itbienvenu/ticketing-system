from pydantic import BaseModel, Field, RootModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic.root_model import RootModel


class TicketCreate(BaseModel):
    user_id: UUID = Field(..., description="ID of the user booking the ticket")
    bus_id: UUID = Field(..., description="ID of the bus")
    route_id: UUID = Field(..., description="ID of the route")

  

class BusInfo(BaseModel):
    plate_number: Optional[str] = None

class RouteInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    price: Optional[float] = None

class TicketResponse(BaseModel):
    id: UUID
    user_id: Optional[str] = None
    full_name:Optional[str] = None
    qr_code: str
    status: str
    created_at: datetime
    mode: str
    route: Optional[str] = None
    bus:Optional[str] = None

    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    root: List[TicketResponse]