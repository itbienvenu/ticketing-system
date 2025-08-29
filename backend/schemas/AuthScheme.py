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
    role_id: int
    permission_ids: List[int]     

class PermissionOut(BaseModel):
    id: str
    name: str    