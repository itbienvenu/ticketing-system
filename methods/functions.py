from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from database.dbs import Base, engine, get_db
from database.models import User
from schemas.LoginRegisteScheme import RegisterUser, LoginUser


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

