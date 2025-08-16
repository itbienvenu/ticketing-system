from fastapi import APIRouter, Depends, HTTPException
from methods.functions import register_route, get_current_user
from database.dbs import get_db
from sqlalchemy.orm import Session
from schemas.RoutesScheme import RegisterRoute, RouteOut
from uuid import UUID
from database.models import Route
from typing import List


router = APIRouter(prefix="/api/v1/routes", tags=['Routes End Points'])

@router.post("/register", response_model=RegisterRoute)
async def register_routes(route: RegisterRoute, db: Session = Depends(get_db) ):
    return register_route(db, route)

@router.get("/{route_id}", response_model=RouteOut, dependencies=[Depends(get_current_user)])
async def get_route_by_id(route_id: UUID, db: Session = Depends(get_db)):
    get_route = db.query(Route).filter(Route.id == str(route_id)).first()
    if not get_route:
        raise HTTPException(status_code=404, detail="Invalid route ID")
    return get_route


@router.get("/", response_model=List[RouteOut], dependencies=[Depends(get_current_user)])
async def get_all_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()
