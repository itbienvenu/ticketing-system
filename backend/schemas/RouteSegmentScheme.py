from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


# Schema for creating a route segment
class RouteSegmentCreate(BaseModel):
    route_id: Optional[str] = Field(default=uuid4(), description="ID of the route this segment belongs to")
    start_station_id: str = Field(..., description="ID of the starting bus station")
    end_station_id: str = Field(..., description="ID of the ending bus station")
    price: float = Field(..., description="Price of traveling this segment")
    stop_order: int = Field(..., description="The order of this segment in the route")

# Schema for updating a route segment
class RouteSegmentUpdate(BaseModel):
    start_station_id: Optional[str] = Field(None, description="ID of the starting bus station")
    end_station_id: Optional[str] = Field(None, description="ID of the ending bus station")
    price: Optional[float] = Field(None, description="Price of traveling this segment")
    stop_order: Optional[int] = Field(None, description="The order of this segment in the route")

# Schema for returning a route segment in responses
class RouteSegmentResponse(BaseModel):
    id: str
    route_id: str
    start_station_id: str
    end_station_id: str
    price: float
    stop_order: int
    company_id: str

    class Config:
        from_attributes = True
