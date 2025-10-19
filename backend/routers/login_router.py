from fastapi import APIRouter, Depends, HTTPException, Body
from methods.functions import create_user, login_user, get_current_user
from methods.permissions import check_permission
from schemas.LoginRegisteScheme import RegisterUser, LoginUser, UpdateUser, UserOut
from database.dbs import get_db
from database.models import *
from sqlalchemy.orm import Session
from typing import List
router = APIRouter(prefix="/api/v1", tags=["User Managment"])

@router.post("/login")
async def login(user: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, user)


@router.post("/register", response_model=UserOut)
async def register(user: RegisterUser, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/me")
async def get_users_me(current_user: User = Depends(get_current_user)):
    role_names = [r.name for r in (current_user.roles or [])]
    primary_role = role_names[0] if role_names else None

    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
        "role": primary_role,   # single role for legacy clients
        "roles": role_names
    }

# Endpoint to delete User

@router.delete("/users/{user_id}", dependencies=[Depends(get_current_user), Depends(check_permission("delete_user"))])
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

@router.patch("/users/{user_id}", response_model=UserOut, dependencies=[Depends(check_permission("update_user"))])
async def update_user(
    user_id: str,
    db: Session = Depends(get_db),
    user: UpdateUser = Body(...),
    current_user = Depends(get_current_user)
):
    get_user = db.query(User).filter(User.id == str(user_id)).first()
    if not get_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update normal fields
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        if key != "role":
            setattr(get_user, key, value)

    # Update role if provided
    if user.role:
        role_obj = db.query(Role).filter(Role.name == user.role).first()
        if not role_obj:
            raise HTTPException(status_code=404, detail="Role not found")
        get_user.roles = [role_obj]  # replace old roles with the new one

    db.commit()
    db.refresh(get_user)

    # Prepare response with role name
    role_name = get_user.roles[0].name if get_user.roles else None
    return UserOut(
        id=get_user.id,
        full_name=get_user.full_name,
        email=get_user.email,
        phone_number=get_user.phone_number,
        role=role_name
    )
   

# Endpoint to get all user
@router.get("/users", response_model=List[UserOut], dependencies=[Depends(check_permission("view_users"))])
def get_all_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    users = db.query(User).all()
    
    result = []
    for u in users:
        # Take the first role name if available
        role_name = u.roles[0].name if u.roles else None
        result.append(UserOut(
            id=u.id,
            full_name=u.full_name,
            email=u.email,
            phone_number=u.phone_number,
            role=role_name
        ))
    
    return result