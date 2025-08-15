from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from database.dbs import Base, engine, get_db
from database.models import User
from schemas.LoginRegisteScheme import RegisterUser, LoginUser
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, UTC

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))   
    to_encode.update({"exp": expire})   
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return encoded_jwt


def create_user(db: Session, user: RegisterUser):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hash(user.password)
    
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def login_user(db: Session, user: LoginUser):

    check_user = None

    if user.email:
        check_user = db.query(User).filter(User.email == user.email).first()

    elif user.phone_number:
        check_user = db.query(User).filter(User.phone_number == user.phone_number).first() 

    if not check_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(user.password, check_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub":str(check_user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "message":"Login Successful",
        "access_token":token,
        "torkn_type": "bearer"
            }