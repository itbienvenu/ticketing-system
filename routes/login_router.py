from fastapi import APIRouter, Depends
from methods.functions import create_user
from schemas.LoginRegisteScheme import RegisterUser
from database.dbs import get_db
from database.models import *
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1", tags=["Login and Registratin"])

@router.get("/login")
async def login():
    return {"message":"Login page"}

@router.post("/register", response_model=RegisterUser)
async def register(user: RegisterUser, db: Session = Depends(get_db)):
    return create_user(db, user)