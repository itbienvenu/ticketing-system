from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.dbs import get_db
from database.models import Schedule, Bus, RouteSegment
from schemas.SchedulesScheme import ScheduleCreate, ScheduleResponse
from methods.functions import get_current_user

router = APIRouter(prefix="/api/v1/schedules", tags=["Schedules"])

#  Create a new schedule
@router.post("/", response_model=ScheduleResponse)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    #  Check if the bus exists and belongs to the same company
    bus = db.query(Bus).filter(
        Bus.id == schedule.bus_id,
        Bus.company_id == current_user.company_id
    ).first()

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    #  Check if the RouteSegment exists and belongs to the same company
    segment = db.query(RouteSegment).filter(
        RouteSegment.id == schedule.route_segment_id,
        RouteSegment.company_id == current_user.company_id
    ).first()

    if not segment:
        raise HTTPException(status_code=404, detail="RouteSegment not found")

    #  Create new schedule
    new_schedule = Schedule(
        bus_id=schedule.bus_id,
        route_segment_id=schedule.route_segment_id,
        departure_time=schedule.departure_time,
        arrival_time=schedule.arrival_time,
        company_id=current_user.company_id
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule



# #  List all schedules (optionally filter by station)
# @router.get("/", response_model=List[ScheduleResponse])
# def list_schedules(route_station_id: str = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     query = db.query(Schedule).filter(Schedule.company_id == current_user.company_id)
#     if route_station_id:
#         query = query.filter(Schedule.route_station_id == route_station_id)
#     return query.all()


# #  Get single schedule
# @router.get("/{schedule_id}", response_model=ScheduleResponse)
# def get_schedule(schedule_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     schedule = db.query(Schedule).filter(
#         Schedule.id == schedule_id,
#         Schedule.company_id == current_user.company_id
#     ).first()
#     if not schedule:
#         raise HTTPException(404, "Schedule not found")
#     return schedule


# #  Update schedule
# @router.put("/{schedule_id}", response_model=ScheduleResponse)
# def update_schedule(schedule_id: str, schedule_update: ScheduleUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     schedule = db.query(Schedule).filter(
#         Schedule.id == schedule_id,
#         Schedule.company_id == current_user.company_id
#     ).first()
#     if not schedule:
#         raise HTTPException(404, "Schedule not found")

#     schedule.departure_time = schedule_update.departure_time
#     schedule.arrival_time = schedule_update.arrival_time
#     db.commit()
#     db.refresh(schedule)
#     return schedule


# #  Delete schedule
# @router.delete("/{schedule_id}")
# def delete_schedule(schedule_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     schedule = db.query(Schedule).filter(
#         Schedule.id == schedule_id,
#         Schedule.company_id == current_user.company_id
#     ).first()
#     if not schedule:
#         raise HTTPException(404, "Schedule not found")

#     db.delete(schedule)
#     db.commit()
#     return {"message": "Schedule deleted successfully"}
