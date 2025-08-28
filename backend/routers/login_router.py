from fastapi import APIRouter, Depends, HTTPException, Body
from methods.functions import create_user, login_user, get_current_user
from schemas.LoginRegisteScheme import RegisterUser, LoginUser, UpdateUser, UserOut
from database.dbs import get_db
from database.models import *
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/api/v1", tags=["User Managment"])

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
        "phone_number":current_user.phone_number,
        "role":current_user.role
    }

# Endpoint to delete User

@router.delete("/users/{user_id}", dependencies=[Depends(get_current_user)])

def delete_user(user_id, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    payments = db.query(Payment).filter(Payment.user_id == user.id).all()
    for payment in payments:
        db.delete(payment)
    db.delete(user)
    db.commit()
    return {"message":f"User with id: {user_id}, deleted well"}

# Endpoint to Edit User

@router.patch("/users/{user_id}",response_model=UpdateUser)
async def update_user(
    user_id: str, 
    db: Session = Depends(get_db), 
    user: UpdateUser = Body(...),
    current_user = Depends(get_current_user)
    ):
    get_user = db.query(User).filter(User.id == str(user_id)).first()

    if not get_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(get_user, key, value)

    db.commit()
    db.refresh(get_user)
    return get_user    

# Endpoint to get all user
@router.get("/users",response_model=List[UserOut], dependencies=[Depends(get_current_user)])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()