from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login_router, routes_router, tickets_router, buses_router
from database.dbs import engine
from database.models import Base
from funs import change_something

app = FastAPI()
change_something()

Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

app.include_router(login_router.router)
app.include_router(routes_router.router)
app.include_router(tickets_router.router)
app.include_router(buses_router.router)

@app.get("/api/v1/")
def home():
    return {"message":"Home Page"}