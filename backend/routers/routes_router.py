from fastapi import APIRouter, Depends, HTTPException, status
from methods.functions import register_route, get_current_user
from methods.permissions import check_permission
from database.dbs import get_db
from sqlalchemy.orm import Session
from schemas.RoutesScheme import RegisterRoute, RouteOut, UpdateRoute, AssignBusRequest
from uuid import UUID
from database.models import Route, Bus
from typing import List
from datetime import datetime, UTC


router = APIRouter(prefix="/api/v1/routes", tags=['Routes End Points'])

@router.post("/register", dependencies=[Depends(check_permission("create_route"))], response_model=RegisterRoute)
async def register_routes(route: RegisterRoute, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Registers a new route, associating it with the user's company.
    """
    # FIX: Access the company_id using dot notation, as the user object is a class instance.
    company_id = user.company_id
    if not company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a company")

    # This is the correct fix for the previous TypeError:
    # We add the company_id to the route object before calling the function.
    route.company_id = company_id
    
    return register_route(db, route)

@router.get("/{route_id}", response_model=RouteOut, dependencies=[Depends(get_current_user)])
async def get_route_by_id(route_id: UUID, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Retrieves a single route by its unique ID, restricted to the user's company.
    """
    # FIX: Use dot notation to access the company_id.
    company_id = user.company_id
    if not company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a company")

    get_route = db.query(Route).filter(
        Route.id == str(route_id),
        Route.company_id == company_id
    ).first()
    
    if not get_route:
        raise HTTPException(status_code=404, detail="Route not found for this company")
    if get_route.created_at is None:
        get_route.created_at = datetime.now(UTC)
    return get_route


@router.get("/", response_model=List[RouteOut], dependencies=[Depends(get_current_user)])
async def get_all_routes(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Retrieves a list of all routes belonging to the user's company.
    """
    # FIX: Use dot notation to access the company_id.
    company_id = user.company_id
    if not company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a company")

    routes = db.query(Route).filter(Route.company_id == company_id).all()
    routes_list = [
        {**r.__dict__, 'created_at': datetime.now(UTC)} if r.created_at is None else r
        for r in routes
    ]
    return routes_list

@router.put("/{route_id}", response_model=UpdateRoute, dependencies=[Depends(check_permission("update_route"))])
async def update_route(route_id: UUID, updated_data: UpdateRoute, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Updates the details of an existing route, restricted to the user's company.
    """
    # FIX: Use dot notation to access the company_id.
    company_id = user.company_id
    if not company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a company")

    get_route = db.query(Route).filter(
        Route.id == str(route_id),
        Route.company_id == company_id
    ).first()
    
    if not get_route:
        raise HTTPException(status_code=404, detail="Route not found for this company")

    for field, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(get_route, field, value)
    get_route.updated_at = datetime.now(UTC)

    db.commit()
    db.refresh(get_route)
    return updated_data

@router.delete("/{route_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(check_permission("delete_route"))])
async def delete_route(route_id: UUID, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Deletes a route, restricted to the user's company.
    """
    # FIX: Use dot notation to access the company_id.
    company_id = user.company_id
    if not company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a company")

    route = db.query(Route).filter(
        Route.id == str(route_id),
        Route.company_id == company_id
    ).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found for this company")
    
    db.delete(route)
    db.commit()

    return {"message": f"Route with ID {route_id} deleted successfully"}

@router.post("/assign-bus", dependencies=[Depends(check_permission("assign_bus_route"))])
async def assign_bus(payload: AssignBusRequest, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Assigns a bus to a route, ensuring both belong to the user's company.
    """
    # FIX: Use dot notation to access the company_id.
    company_id = user.company_id
    if not company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a company")

    # find route for the user's company
    route = db.query(Route).filter(
        Route.id == str(payload.route_id),
        Route.company_id == company_id
    ).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found for this company")

    # find bus for the user's company
    bus = db.query(Bus).filter(
        Bus.id == str(payload.bus_id),
        Bus.company_id == company_id
    ).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found for this company")

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
