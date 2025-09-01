from fastapi import APIRouter, Depends, HTTPException, status
from database.models import Role, Permission,User
from methods.functions import get_current_user
from database.dbs import get_db
from sqlalchemy.orm import aliased, joinedload
from methods.permissions import check_permission
from sqlalchemy.orm import Session
from schemas.AuthScheme import RoleCreate, PermissionCreate, RolePermissionAssign, PermissionOut, MyPermissionsOut, RoleOut
from typing import List

router = APIRouter(prefix="/api/v1/perm", tags=['Permission control endpoints'])

@router.get("/validate-token")
async def validate_token(current_user = Depends(get_current_user)):
    return {"status": "valid", "user_id": current_user.id}


@router.post("/create_permission", dependencies=[Depends(check_permission("create_permission"))])
def create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Check if permission with the same name exists
    """Admins are only to  access this role"""

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




@router.get("/get_permissions", response_model=List[PermissionOut], dependencies=[Depends(check_permission("get_permission"))])
def get_permissions(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Any one can access this enpoint to see his permission, but mostly for admins class"""
    return db.query(Permission).all()

# Role managment
@router.get("/my_permissions", response_model=MyPermissionsOut)
def my_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    permissions = (
        db.query(Permission)
        .filter(Permission.roles.any(Role.users.any(User.id == current_user.id)))
        .all()
    )

    return {
        # "user_id": current_user.id,
        # "user_full_name": current_user.full_name,
        # "email":current_user.email,
        "permissions": [{"id": p.id, "name": p.name} for p in permissions]
    }



# Assigning the 
@router.post("/assign_permissions", dependencies=[Depends(check_permission("assign_permission"))])
def assign_permissions_to_role(
    data: RolePermissionAssign,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Eagerly load the permissions relationship to ensure they are in the session
    role = db.query(Role).filter(Role.id == data.role_id).options(joinedload(Role.permissions)).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Fetch the single permission to assign
    permission_to_add = db.query(Permission).filter(Permission.id == data.permission_id).first()
    if not permission_to_add:
        raise HTTPException(status_code=404, detail="Permission not found with the provided ID")

    # Check if the permission is already assigned to the role
    existing_permission_ids = {p.id for p in role.permissions}
    if permission_to_add.id in existing_permission_ids:
        return {
            "message": f"Permission with ID '{permission_to_add.id}' is already assigned to role '{role.name}'",
            "role": {
                "id": role.id,
                "name": role.name,
                "permissions": [{"id": p.id, "name": p.name} for p in role.permissions]
            }
        }

    # Add the new permission to the role's collection
    role.permissions.append(permission_to_add)

    # Commit the changes to the database
    db.commit()
    db.refresh(role)

    return {
        "message": f"Permission '{permission_to_add.name}' assigned to role '{role.name}' successfully",
        "role": {
            "id": role.id,
            "name": role.name,
            "permissions": [{"id": p.id, "name": p.name} for p in role.permissions]
        }
    }



# Deleting the Permission
@router.delete("/delete_permission/{permission_id}", dependencies=[Depends(check_permission("delete_permission"))])
def delete_role(
    permission_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Find the role to delete
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    # Check if the role exists
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Delete the Permissionrole
    db.delete(permission)
    db.commit()

    return {"message": f"Role '{permission.name}' with ID '{permission_id}' deleted successfully"}

