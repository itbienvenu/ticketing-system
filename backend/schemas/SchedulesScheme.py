from datetime import datetime
from typing import Optional

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
