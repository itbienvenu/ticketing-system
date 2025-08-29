from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Bus, Route, bus_routes, Payment, User
from database.dbs import get_db  
from schemas.BusesScheme import BusCreate, BusOut, UpdateBus
from uuid import uuid4, UUID
from typing import List
from methods.functions import get_current_user
from datetime import datetime, UTC
router = APIRouter(prefix="/api/v1/buses", tags=["Buses"])

# Creating the buss

def require_roles(allowed_roles: list[str]):
    def decorator(user: User = Depends(get_current_user)):
        user_roles = [ur.role.name for ur in user.roles]
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return decorator


@router.post("/", dependencies=[Depends(get_current_user)])
async def create_bus(bus: BusCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new bus.
    Routes are optional — they can be attached later.
    """
    # Check if plate number already exists
    existing_bus = db.query(Bus).filter(Bus.plate_number == bus.plate_number).first()
    if existing_bus:
        raise HTTPException(status_code=400, detail="Bus with this plate number already exists")

    # Create new bus
    new_bus = Bus(
        id=str(uuid4()),
        plate_number=bus.plate_number,
        seats=bus.seats,
        created_at=datetime.now(UTC)
    )

    # Attach routes only if provided
    if bus.route_ids:
        routes = db.query(Route).filter(Route.id.in_([str(rid) for rid in bus.route_ids])).all()
        if not routes or len(routes) != len(bus.route_ids):
            raise HTTPException(status_code=404, detail="One or more routes not found")
        new_bus.routes = routes

    # Save
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)

    return {
        "message": "Bus registered successfully",
        "bus_id": new_bus.id,
        "attached_routes": [r.id for r in new_bus.routes]  # helpful info
    }

@router.get("/by-route/{route_id}", response_model=List[BusOut], dependencies=[Depends(get_current_user)])
async def get_buses_by_route(route_id: UUID, db: Session = Depends(get_db)):
    # fetch route
    route = db.query(Route).filter(Route.id == str(route_id)).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # return buses with route_ids
    result = []
    for bus in route.buses:
        result.append(BusOut(
            id=bus.id,
            plate_number=bus.plate_number,
            seats=bus.seats,
            created_at=bus.created_at,
            route_ids=[r.id for r in bus.routes]
        ))
    return result
# Endpoint to list all buses

@router.get("/", response_model=List[BusOut], dependencies=[Depends(get_current_user)])
async def get_all_buses(db: Session = Depends(get_db)):
    buses = db.query(Bus).all()
    result = []

    for bus in buses:
        route_ids = [
            r.route_id
            for r in db.query(bus_routes).filter(bus_routes.c.bus_id == bus.id).all()
        ]
        bus_dict = {
            "id": bus.id,
            "plate_number": bus.plate_number,
            "seats": bus.seats,
            "created_at": bus.created_at,
            "route_ids": route_ids,
        }
        result.append(bus_dict)

    return result


# Updating the bus

@router.patch("/{bus_id}", dependencies=[Depends(get_current_user)])
def update_bus(bus_id: str, bus_update: UpdateBus, db: Session = Depends(get_db)):
    # Fetch the bus
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # Update only fields that are provided
    if bus_update.plate_number is not None:
        bus.plate_number = bus_update.plate_number
    if bus_update.seats is not None:
        bus.seats = bus_update.seats
    if bus_update.route_ids is not None:
        bus.route_ids = bus_update.route_ids

    db.commit()
    db.refresh(bus)  # refresh to get updated object
    return bus

# Endpoint to delete the Bus

@router.delete("/{bus_id}", dependencies=[Depends(get_db)])

def delete_bus(bus_id: str, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    db.delete(bus)
    db.commit()

    return {
        "message":f"Deleted bus with id: {bus_id}"
        }