from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from database.dbs import Base, engine, get_db
from database.models import User, Route
from schemas.LoginRegisteScheme import RegisterUser, LoginUser
from schemas.RoutesScheme import RegisterRoute, UpdateRoute, RouteOut
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, UTC

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
# oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
bearer_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))   
    to_encode.update({"exp": expire})   
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session =  Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
    return user


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
        "token_type": "bearer"
            }

def register_route(db: Session, route: RegisterRoute):
    check_route = (db.query(Route)
    .filter(Route.origin == route.origin)
    .filter(Route.destination == route.destination)
    .first()
    )
    if check_route:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Route is alredy registered")
    
    db_route = Route(
        origin = route.origin,
        destination = route.destination,
        price = route.price,
        created_at = datetime.now(UTC)
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route
        
    