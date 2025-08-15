from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Login and Registratin"])

@router.get("/login")
async def login():
    return {"message":"Login page"}

@router.get("/register")

async def register():
    return {"message":"Register Page"}