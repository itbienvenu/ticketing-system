from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Bus, Route
from database.dbs import get_db  
from schemas.BusesScheme import BusCreate, BusOut
from uuid import uuid4, UUID
from typing import List
from methods.functions import get_current_user
from datetime import datetime, UTC
router = APIRouter(prefix="/api/v1/buses", tags=["Buses"])

@router.post("/", dependencies=[Depends(get_current_user)])
async def create_bus(bus: BusCreate, db: Session = Depends(get_db)):
    # Check if plate number already exists
    existing_bus = db.query(Bus).filter(Bus.plate_number == bus.plate_number).first()
    if existing_bus:
        raise HTTPException(status_code=400, detail="Bus with this plate number already exists")

    # Create new bus
    new_bus = Bus(
        id=str(uuid4()),
        plate_number=bus.plate_number,
        created_at=datetime.now(UTC)
    )

    # Attach routes
    routes = db.query(Route).filter(Route.id.in_([str(rid) for rid in bus.route_ids])).all()
    if not routes or len(routes) != len(bus.route_ids):
        raise HTTPException(status_code=404, detail="One or more routes not found")
    new_bus.routes = routes

    # Save
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)

    return {"message": "Bus registered successfully", "bus_id": new_bus.id}


@router.get("/by-route/{route_id}", response_model=List[BusOut], dependencies=[Depends(get_current_user)])
async def get_buses_by_route(route_id: UUID, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == str(route_id)).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return [
        BusOut(
            id=bus.id,
            plate_number=bus.plate_number,
            created_at=bus.created_at,
            route_ids=[r.id for r in bus.routes]
        )
        for bus in route.buses
    ]


@router.get("/", response_model=List[BusOut], dependencies=[Depends(get_current_user)])
async def get_all_buses(db: Session = Depends(get_db)):
    return db.query(Bus).all()