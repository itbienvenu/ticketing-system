from fastapi import APIRouter, Depends, HTTPException, status
from database.models import Role, Permission
from methods.functions import get_current_user
from database.dbs import get_db
from methods.permissions import check_permission
from sqlalchemy.orm import Session
from schemas.AuthScheme import RoleCreate, PermissionCreate, RolePermissionAssign, PermissionOut
from typing import List
router = APIRouter(prefix="/api/v1", tags=['Authorization endpoints'])

@router.get("/validate-token")
async def validate_token(current_user = Depends(get_current_user)):
    return {"status": "valid", "user_id": current_user.id}

# Endpoint to create roles
@router.post("/create_role", dependencies=[Depends(check_permission("create_role"))])
def create_role(role_data: RoleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Check if role with same name exists
    existing = db.query(Role).filter(Role.name == role_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists"
        )
    
    # Create Role
    new_role = Role(name=role_data.name)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return {"message": "Role created successfully", "role": {"id": new_role.id, "name": new_role.name}}

@router.post("/create_permission", dependencies=[Depends(check_permission("create_permission"))])
def create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Check if permission with the same name exists
    existing = db.query(Permission).filter(Permission.name == permission_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission with this name already exists"
        )
    
    # Create Permission
    new_permission = Permission(name=permission_data.name)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    return {"message": "Permission created successfully", "permission": {"id": new_permission.id, "name": new_permission.name}}


@router.post("/assign_permissions", dependencies=[Depends(check_permission("assign_permission"))])
def assign_permissions_to_role(data: RolePermissionAssign, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Fetch role
    role = db.query(Role).filter(Role.id == data.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Fetch permissions
    permissions = db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
    if not permissions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No valid permissions found for the provided IDs"
        )
    
    # Assign permissions
    role.permissions = permissions
    db.commit()
    db.refresh(role)

    return {
        "message": f"Permissions assigned to role '{role.name}' successfully",
        "role": {
            "id": role.id,
            "name": role.name,
            "permissions": [{"id": p.id, "name": p.name} for p in role.permissions]
        }
    }


@router.get("/get_permissions", response_model=List[PermissionOut], dependencies=[Depends(check_permission("get_permission"))])
def get_permissions(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(Permission).all()

# Role managment
