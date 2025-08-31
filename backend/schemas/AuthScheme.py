from pydantic import BaseModel
from typing import List

# Roles

class RoleCreate(BaseModel):
    name: str

class RoleOut(BaseModel):
    id: str
    name: str

# Permissions

class PermissionCreate(BaseModel):
    name: str

class RolePermissionAssign(BaseModel):
    role_id: str
    permission_id: str    

class PermissionOut(BaseModel):
    id: str
    name: str    

class MyPermissionsOut(BaseModel):
    # user_id: str
    # user_full_name: str
    # email: str
    permissions: list[PermissionOut]  # each dict contains "id" and "name" of a permission
