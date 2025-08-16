from fastapi import APIRouter, Depends
from methods.functions import register_route
from database.dbs import get_db
from sqlalchemy.orm import Session
from schemas.RoutesScheme import RegisterRoute

router = APIRouter(prefix="/api/v1/routes", tags=['Routes End Points'])

@router.post("/register", response_model=RegisterRoute)
def register_routes(route: RegisterRoute, db: Session = Depends(get_db) ):
    return register_route(db, route)