"""hy"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login_router, routes_router, tickets_router, buses_router, auth_router, payments_router
from database.dbs import engine
from database.models import Base
import uvicorn

app = FastAPI(
    docs_url="/documentation",
    redoc_url=None,
    # openapi_url=None
)

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

# Include routers
app.include_router(auth_router.router)
app.include_router(login_router.router)
app.include_router(routes_router.router)
app.include_router(tickets_router.router)
app.include_router(buses_router.router)
app.include_router(payments_router.router)

# Home route
@app.get("/api/v1/")
def home():
    """The home route"""
    return {"message": "Home Page"}
