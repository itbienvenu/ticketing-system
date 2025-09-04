from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Bus, Route, bus_routes, Payment, User
from database.dbs import get_db
from schemas.BusesScheme import BusCreate, BusOut, UpdateBus
from uuid import uuid4, UUID
from typing import List
# from methods.functions import get_current_company_user  # Renamed for clarity
from methods.permissions import check_permission, get_current_company_user
from datetime import datetime, UTC

router = APIRouter(prefix="/api/v1/buses", tags=["Buses"])

@router.post("/", dependencies=[Depends(get_current_company_user)])
async def create_bus(
    bus: BusCreate,
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint to create a new bus for the current user's company.
    Routes are optional — they can be attached later.
    """
    # Check if plate number already exists within the user's company
    existing_bus = db.query(Bus).filter(
        Bus.plate_number == bus.plate_number,
        Bus.company_id == current_user.company_id
    ).first()
    if existing_bus:
        raise HTTPException(status_code=400, detail="Bus with this plate number already exists for your company.")

    # Create new bus
    new_bus = Bus(
        id=str(uuid4()),
        plate_number=bus.plate_number,
        capacity=bus.capacity,
        created_at=datetime.now(UTC),
        company_id=current_user.company_id  # Associate bus with the user's company
    )

    # Attach routes only if provided
    if bus.route_ids:
        # Filter routes by company_id to prevent cross-company route assignment
        routes = db.query(Route).filter(
            Route.id.in_([str(rid) for rid in bus.route_ids]),
            Route.company_id == current_user.company_id
        ).all()
        if not routes or len(routes) != len(bus.route_ids):
            raise HTTPException(status_code=404, detail="One or more routes not found or not part of your company.")
        new_bus.routes = routes

    # Save
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)

    return {
        "message": "Bus registered successfully",
        "bus_id": new_bus.id,
        "attached_routes": [r.id for r in new_bus.routes]
    }

@router.get("/by-route/{route_id}", response_model=List[BusOut], dependencies=[Depends(get_current_company_user)])
async def get_buses_by_route(
    route_id: UUID,
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    """
    Returns a list of buses for a specific route, ensuring the route belongs to the user's company.
    """
    # Fetch route and filter by company_id
    route = db.query(Route).filter(
        Route.id == str(route_id),
        Route.company_id == current_user.company_id
    ).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found or not part of your company.")

    # Return buses related to the route, which are already filtered by the route's company_id
    result = []
    for bus in route.buses:
        result.append(BusOut(
            id=bus.id,
            plate_number=bus.plate_number,
            capacity=bus.capacity,
            available_seats=bus.capacity - bus.available_seats,
            created_at=bus.created_at,
            route_ids=[r.id for r in bus.routes]
        ))
    return result

# Endpoint to list all buses
@router.get("/", response_model=List[BusOut], dependencies=[Depends(get_current_company_user)])
async def get_all_buses(
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    """
    Returns a list of all buses for the current user's company.
    """
    buses = db.query(Bus).filter(Bus.company_id == current_user.company_id).all()
    result = []
    for bus in buses:
        bus_dict = {
            "id": bus.id,
            "plate_number": bus.plate_number,
            "capacity": bus.capacity,
            "available_seats": bus.capacity - bus.available_seats,
            "created_at": bus.created_at,
            "route_ids": [r.id for r in bus.routes],
        }
        result.append(bus_dict)
    return result

# Updating the bus
@router.patch("/{bus_id}", dependencies=[Depends(get_current_company_user)])
def update_bus(
    bus_id: str,
    bus_update: UpdateBus,
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    """
    Updates a bus, ensuring it belongs to the user's company.
    """
    # Fetch the bus and filter by company_id
    bus = db.query(Bus).filter(
        Bus.id == bus_id,
        Bus.company_id == current_user.company_id
    ).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found or not part of your company.")

    # Update only fields that are provided
    if bus_update.plate_number is not None:
        bus.plate_number = bus_update.plate_number
    if bus_update.capacity is not None:
        bus.capacity = bus_update.capacity
    if bus_update.route_ids is not None:
        # Filter new routes by company_id to prevent cross-company route association
        routes = db.query(Route).filter(
            Route.id.in_([str(rid) for rid in bus_update.route_ids]),
            Route.company_id == current_user.company_id
        ).all()
        if not routes or len(routes) != len(bus_update.route_ids):
            raise HTTPException(status_code=404, detail="One or more routes not found or not part of your company.")
        bus.routes = routes

    db.commit()
    db.refresh(bus)
    return bus

# Endpoint to delete the Bus
@router.delete("/{bus_id}", dependencies=[Depends(get_current_company_user), Depends(check_permission("delete_bus"))])
def delete_bus(
    bus_id: str,
    current_user: User = Depends(get_current_company_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a bus, ensuring it belongs to the user's company.
    """
    # Find the bus and filter by company_id
    bus = db.query(Bus).filter(
        Bus.id == bus_id,
        Bus.company_id == current_user.company_id
    ).first()

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found or not part of your company.")
    
    db.delete(bus)
    db.commit()

    return {
        "message": f"Deleted bus with id: {bus_id}"
    }

# ---

### Key Changes and Rationale

# * **`get_current_company_user` Dependency**: This new dependency is used in every endpoint. It validates that the user is not only authenticated but is also a staff member of a company. This is the **primary security measure** for data isolation.
# * **Data Filtering**: All SQLAlchemy queries (`.filter()`) now include the condition `Bus.company_id == current_user.company_id`. This guarantees that a company user can only perform operations on buses and routes that belong to their company.
# * **Plate Number Uniqueness**: The `create_bus` endpoint's uniqueness check has been updated to be specific to the company: `Bus.plate_number == bus.plate_number, Bus.company_id == current_user.company_id`. This allows different companies to use the same plate number without conflicts.
# * **Route Association**: In the `create_bus` and `update_bus` endpoints, when attaching or updating routes, an additional filter `Route.company_id == current_user.company_id` is applied. This prevents a user from associating their bus with a route from another company.
# * **Permission Check**: The `check_permission` dependency remains useful for role-based access control within a company (e.g., only a "manager" can delete a bus). The new `get_current_company_user` dependency ensures that even with the correct role, a user can only affect resources within their own company.

# This refactored file is a complete solution for bus management in your multi-tenant system.