from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Bus  
from database.dbs import get_db  
from schemas.BusesScheme import BusCreate, BusOut
from uuid import uuid4
from typing import List
from methods.functions import get_current_user

router = APIRouter(prefix="/api/v1/buses", tags=["Buses"])

@router.post("/", dependencies=[Depends(get_current_user)])
async def create_bus(bus: BusCreate, db: Session = Depends(get_db)):
    # Check if plate number already exists
    existing_bus = db.query(Bus).filter(Bus.plate_number == bus.plate_number).first()
    if existing_bus:
        raise HTTPException(status_code=400, detail="Bus with this plate number already exists")

    new_bus = Bus(
        id =  str(uuid4()),
        plate_number=bus.plate_number
    )
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return {"message": "Bus registered successfully", "bus_id": new_bus.id}

@router.get("/", response_model=List[BusOut], dependencies=[Depends(get_current_user)])
async def get_all_buses(db: Session = Depends(get_db)):
    return db.query(Bus).all()