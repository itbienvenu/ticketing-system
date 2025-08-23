from fastapi import APIRouter, Depends
from methods.functions import get_current_user


router = APIRouter(prefix="/api/v1", tags=['Authorization endpoints'])

@router.get("/validate-token")
async def validate_token(current_user = Depends(get_current_user)):
    return {"status": "valid", "user_id": current_user.id}

