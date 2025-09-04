from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, UTC
import uuid

from  database.dbs import get_db
from database.models import Company, User, Role, Permission
from schemas.CompanyScheme import CompanyCreate, CompanyResponse, UserCreate, PasswordChange
# from app.dependencies.dependencies import get_current_super_admin_user
# from app.utils.auth_utils import get_password_hash
from methods.functions import get_current_user
from passlib.hash import bcrypt


# Define a new router for company management
router = APIRouter(prefix="/companies", tags=["Companies"])

def get_current_super_admin_user(current_user: User = Depends(get_current_user)):
    if not any(role.name == "super_admin" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return current_user

@router.post(
    "/create_company",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_super_admin_user)]
)
async def create_new_company_with_admin(
    company_data: CompanyCreate,
    admin_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Creates a new company and its first super admin user.
    This endpoint is for the main system admin.
    """
    # 1. Check if company name or email already exists
    if db.query(Company).filter(Company.name == company_data.name).first():
        raise HTTPException(status_code=400, detail="Company name already registered.")
    if db.query(Company).filter(Company.email == company_data.email).first():
        raise HTTPException(status_code=400, detail="Company email already registered.")
    
    # 2. Check if the initial admin user's email already exists
    if db.query(User).filter(User.email == admin_data.email).first():
        raise HTTPException(status_code=400, detail="Admin email already in use.")

    try:
        # 3. Create the new company
        new_company = Company(
            id=str(uuid.uuid4()),
            name=company_data.name,
            email=company_data.email,
            phone_number=company_data.phone_number,
            address=company_data.address,
            created_at=datetime.now(UTC)
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        # 4. Create the new company's admin user
        hashed_password = bcrypt.hash(admin_data.password)
        new_admin_user = User(
            id=str(uuid.uuid4()),
            full_name=admin_data.full_name,
            email=admin_data.email,
            phone_number=admin_data.phone_number,
            password_hash=hashed_password,
            created_at=datetime.now(UTC),
            company_id=new_company.id  # Associate user with the new company
        )

        # 5. Assign the 'company_admin' role to the new user
        company_admin_role = db.query(Role).filter(Role.name == "company_admin").first()
        if not company_admin_role:
            raise HTTPException(
                status_code=500,
                detail="System error: 'company_admin' role not found. Please create it."
            )
        new_admin_user.roles.append(company_admin_role)
        db.add(new_admin_user)
        db.commit()
        
        return new_company

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.get(
    "/",
    response_model=List[CompanyResponse],
    dependencies=[Depends(get_current_super_admin_user)]
)
async def get_all_companies(db: Session = Depends(get_db)):
    """
    Returns a list of all companies. Accessible only by a super admin.
    """
    companies = db.query(Company).all()
    return companies

@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
    dependencies=[Depends(get_current_super_admin_user)]
)
async def get_company_by_id(company_id: str, db: Session = Depends(get_db)):
    """
    Returns a single company by its ID. Accessible only by a super admin.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company