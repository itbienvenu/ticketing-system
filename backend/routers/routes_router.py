from fastapi import APIRouter, Depends, HTTPException
from methods.functions import register_route, get_current_user
from database.dbs import get_db
from sqlalchemy.orm import Session
from schemas.RoutesScheme import RegisterRoute, RouteOut, UpdateRoute, AssignBusRequest
from uuid import UUID
from database.models import Route, Bus
from typing import List
from datetime import datetime, UTC


router = APIRouter(prefix="/api/v1/routes", tags=['Routes End Points'])

@router.post("/register", response_model=RegisterRoute)
async def register_routes(route: RegisterRoute, db: Session = Depends(get_db) ):
    return register_route(db, route)

@router.get("/{route_id}", response_model=RouteOut, dependencies=[Depends(get_current_user)])
async def get_route_by_id(route_id: UUID, db: Session = Depends(get_db)):
    get_route = db.query(Route).filter(Route.id == str(route_id)).first()
    if not get_route:
        raise HTTPException(status_code=404, detail="Invalid route ID")
    if get_route.created_at == None:
        get_route.created_at = datetime.now(UTC)
    return get_route


@router.get("/", response_model=List[RouteOut], dependencies=[Depends(get_current_user)])
async def get_all_routes(db: Session = Depends(get_db)):
    routes =  db.query(Route).all()
    routes_list = []
    for r in routes:
        if r.created_at == None:
            r.created_at = datetime.now(UTC)
        routes_list.append(r)
    return routes_list    

@router.put("/{route_id}", response_model=UpdateRoute, dependencies=[Depends(get_current_user)])
async def update_route(route_id: UUID, updated_data: UpdateRoute,  db: Session = Depends(get_db)):
    get_route = db.query(Route).filter(Route.id == str(route_id)).first()
    if not get_route:
        raise HTTPException(status_code=404, detail="Invalid Route ID")
    
    for field, value in updated_data.model_dump(exclude_unset=True).items():    
        setattr(get_route, field, value)    
    get_route.updated_at = datetime.now(UTC)

    db.commit()
    db.refresh(get_route)
    return updated_data    

# Endpoint to delete route

@router.delete("/{route_id}", dependencies=[Depends(get_current_user)])

async def delete_route(route_id: str, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route_id:
        raise HTTPException(status_code=403, detail="Route not found")
    db.delete(route)
    db.commit()

    return {"message":f"Route with {route_id} deleted well"}

# Assign bus to routes endpoint

@router.post("/assign-bus", dependencies=[Depends(get_current_user)])
def assign_bus(payload: AssignBusRequest, db: Session = Depends(get_db)):
    # find route
    route = db.query(Route).filter(Route.id == str(payload.route_id)).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # find bus
    bus = db.query(Bus).filter(Bus.id == str(payload.bus_id)).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # check if already assigned
    if bus in route.buses:
        raise HTTPException(status_code=400, detail="Bus already assigned to this route")

    # assign
    route.buses.append(bus)
    db.commit()
    db.refresh(route)

    return {
        "message": "Bus assigned successfully",
        "route_id": route.id,
        "bus_id": bus.id,
        "assigned_buses": [b.id for b in route.buses]
    }