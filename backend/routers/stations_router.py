from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.models import BusStation, Schedule, Ticket, User
from schemas.StationsScheme import BusStationCreate, BusStationResponse, ScheduleCreate, ScheduleResponse
from methods.permissions import get_current_company_user, check_permission
from database.dbs import get_db

router = APIRouter(prefix="/api/v1/stations", tags=['Bus Stations Endpoints'])



@router.post("/", response_model=BusStationResponse)
def create_station(
    station: BusStationCreate,
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    new_station = BusStation(
        name=station.name,
        location=station.location,
        company_id=current_user.company_id
    )
    db.add(new_station)
    db.commit()
    db.refresh(new_station)
    return new_station

# # To list stations

@router.get("/", response_model=List[BusStationResponse])
def list_stations(
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    return db.query(BusStation).filter(BusStation.company_id == current_user.company_id).all()

# # To delete any station

@router.delete("/{station_id}")
def delete_station(
    station_id: str,
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    station = db.query(BusStation).filter(
        BusStation.id == station_id,
        BusStation.company_id == current_user.company_id
    ).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    db.delete(station)
    db.commit()
    return {"message": f"Deleted station {station_id}"}

# # Add route to station

# @router.post("/routes/{route_id}/stations", response_model=RouteStationResponse)
# def add_station_to_route(
#     route_id: str,
#     data: RouteStationCreate,
#     current_user: User = Depends(get_current_company_user),
#     db: Session = Depends(get_db)
# ):
#     route_station = RouteStation(
#         route_id=route_id,
#         station_id=data.station_id,
#         stop_order=data.stop_order,
#         company_id=current_user.company_id
#     )
#     db.add(route_station)
#     db.commit()
#     db.refresh(route_station)
#     return route_station

# @router.get("/routes/{route_id}/stations", response_model=List[RouteStationResponse])
# def list_route_stations(
#     route_id: str,
#     current_user: User = Depends(get_current_company_user),
#     db: Session = Depends(get_db)
# ):
#     return (
#         db.query(RouteStation)
#         .filter(RouteStation.route_id == route_id, RouteStation.company_id == current_user.company_id)
#         .order_by(RouteStation.stop_order)
#         .all()
#     )

# @router.delete("/routes/stations/{route_station_id}")
# def delete_route_station(
#     route_station_id: str,
#     current_user: User = Depends(get_current_company_user),
#     db: Session = Depends(get_db)
# ):
#     rs = db.query(RouteStation).filter(
#         RouteStation.id == route_station_id,
#         RouteStation.company_id == current_user.company_id
#     ).first()
#     if not rs:
#         raise HTTPException(status_code=404, detail="RouteStation not found")
#     db.delete(rs)
#     db.commit()
#     return {"message": f"Deleted route station {route_station_id}"}

# @router.post("/routes/stations/{route_station_id}/schedules", response_model=ScheduleResponse)
# def create_schedule(
#     route_station_id: str,
#     data: ScheduleCreate,
#     current_user: User = Depends(get_current_company_user),
#     db: Session = Depends(get_db)
# ):
#     schedule = Schedule(
#         route_station_id=route_station_id,
#         departure_time=data.departure_time,
#         arrival_time=data.arrival_time,
#         company_id=current_user.company_id
#     )
#     db.add(schedule)
#     db.commit()
#     db.refresh(schedule)
#     return schedule

# @router.get("/routes/{route_id}/schedules", response_model=List[ScheduleResponse])
# def list_route_schedules(
#     route_id: str,
#     current_user: User = Depends(get_current_company_user),
#     db: Session = Depends(get_db)
# ):
#     return (
#         db.query(Schedule)
#         .join(RouteStation, Schedule.route_station_id == RouteStation.id)
#         .filter(RouteStation.route_id == route_id, RouteStation.company_id == current_user.company_id)
#         .order_by(RouteStation.stop_order)
#         .all()
#     )
