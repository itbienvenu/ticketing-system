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
    permission_ids: List[str]     

class PermissionOut(BaseModel):
    id: str
    name: str    