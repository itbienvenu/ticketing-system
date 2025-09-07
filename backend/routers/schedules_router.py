# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from database.dbs import get_db
# from database.models import Schedule, RouteStation
# from schemas.SchedulesScheme import ScheduleCreate, ScheduleUpdate, ScheduleResponse
# from methods.functions import get_current_user

# router = APIRouter(prefix="/schedules", tags=["Schedules"])

# # ✅ Create a new schedule
# @router.post("/", response_model=ScheduleResponse)
# def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     route_station = db.query(RouteStation).filter(
#         RouteStation.id == schedule.route_station_id,
#         RouteStation.company_id == current_user.company_id
#     ).first()

#     if not route_station:
#         raise HTTPException(404, "RouteStation not found")

#     new_schedule = Schedule(
#         route_station_id=schedule.route_station_id,
#         departure_time=schedule.departure_time,
#         arrival_time=schedule.arrival_time,
#         company_id=current_user.company_id
#     )
#     db.add(new_schedule)
#     db.commit()
#     db.refresh(new_schedule)
#     return new_schedule


# # ✅ List all schedules (optionally filter by station)
# @router.get("/", response_model=List[ScheduleResponse])
# def list_schedules(route_station_id: str = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     query = db.query(Schedule).filter(Schedule.company_id == current_user.company_id)
#     if route_station_id:
#         query = query.filter(Schedule.route_station_id == route_station_id)
#     return query.all()


# # ✅ Get single schedule
# @router.get("/{schedule_id}", response_model=ScheduleResponse)
# def get_schedule(schedule_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     schedule = db.query(Schedule).filter(
#         Schedule.id == schedule_id,
#         Schedule.company_id == current_user.company_id
#     ).first()
#     if not schedule:
#         raise HTTPException(404, "Schedule not found")
#     return schedule


# # ✅ Update schedule
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


# # ✅ Delete schedule
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
