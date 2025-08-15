from fastapi import APIRouter, Depends
from methods.functions import create_user, login_user
from schemas.LoginRegisteScheme import RegisterUser, LoginUser
from database.dbs import get_db
from database.models import *
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1", tags=["Login and Registratin"])

@router.post("/login")
async def login(user: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, user)


@router.post("/register", response_model=RegisterUser)
async def register(user: RegisterUser, db: Session = Depends(get_db)):
    return create_user(db, user)