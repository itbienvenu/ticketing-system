from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from methods.functions import get_current_user
from database.dbs import get_db
from database.models import Permission, Role, User

def check_permission(permission_name: str):
    def wrapper(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
        # Join Permission → Role → User
        user_permissions = (
            db.query(Permission.name)
            .join(Permission.roles)  # Permission → Role
            .join(Role.users)        # Role → User
            .filter(User.id == current_user.id)  # Only current user
            .all()
        )

        allowed = any(p[0] == permission_name for p in user_permissions)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
            )
        return True
    return wrapper

