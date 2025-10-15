from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleBase(BaseModel):
    bus_id: str
    route_segment_id: str
    departure_time: datetime
    arrival_time: datetime

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    departure_time: datetime
    arrival_time: datetime

class ScheduleResponse(ScheduleBase):
    id: str
    company_id: str

    class Config:
        from_attributes = True
