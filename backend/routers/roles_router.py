from fastapi import APIRouter, Depends, HTTPException, status
from database.models import Role, Permission,User
from methods.functions import get_current_user
from database.dbs import get_db
from sqlalchemy.orm import aliased, joinedload
from methods.permissions import check_permission
from sqlalchemy.orm import Session
from schemas.AuthScheme import RoleCreate, PermissionCreate, RolePermissionAssign, PermissionOut, MyPermissionsOut, RoleOut
from typing import List

router = APIRouter(prefix="/api/v1/roles", tags=['Roles control endpoints'])

# Endpoint to create roles
@router.post("/create_role", dependencies=[Depends(check_permission("create_role"))])
def create_role(role_data: RoleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Check if role with same name exists
    """Admins are only to  access this role"""

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

# Getting all roles

@router.get("/all_roles", response_model=List[RoleOut], dependencies=[Depends(check_permission("list_all_roles"))])
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


# Deleting the role
@router.delete("/delete_role/{role_id}", dependencies=[Depends(check_permission("delete_role"))])
def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Find the role to delete
    role = db.query(Role).filter(Role.id == role_id).first()
    
    # Check if the role exists
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Delete the role
    db.delete(role)
    db.commit()

    return {"message": f"Role '{role.name}' with ID '{role_id}' deleted successfully"}

