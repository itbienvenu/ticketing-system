from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BusStationBase(BaseModel):
    name: str
    location: Optional[str] = None


class BusStationCreate(BusStationBase):
    pass

# Response schema
class BusStationResponse(BusStationBase):
    id: str
    created_at: datetime
    company_id: str

    class Config:
        orm_mode = True

class RouteStationBase(BaseModel):
    stop_order: int

# Create schema (company_id inferred from current_user)
class RouteStationCreate(RouteStationBase):
    station_id: str  # the bus station ID

# Response schema
class RouteStationResponse(RouteStationBase):
    id: str
    route_id: str
    station_id: str
    company_id: str

    class Config:
        orm_mode = True



class ScheduleBase(BaseModel):
    departure_time: datetime
    arrival_time: Optional[datetime] = None

# Create schema (company_id inferred from current_user)
class ScheduleCreate(ScheduleBase):
    route_station_id: str  # the route station ID

# Response schema
class ScheduleResponse(ScheduleBase):
    id: str
    route_station_id: str
    company_id: str

    class Config:
        orm_mode = True
