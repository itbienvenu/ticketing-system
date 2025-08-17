from fastapi import APIRouter, Depends
from methods.functions import create_user, login_user, get_current_user
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

@router.get("/me")
async def get_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id":str(current_user.id),
        "full_name": current_user.full_name,
        "email":current_user.email,
        "phone_number":current_user.phone_number
    }