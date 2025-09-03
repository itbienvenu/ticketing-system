from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Float, Enum
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.dbs import Base
import uuid
from datetime import datetime, UTC
import enum

# Association table: roles <-> permissions (many-to-many)
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", String, ForeignKey("permissions.id"), primary_key=True),
)

# Association table: users <-> roles (if multi-role support)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

    # 🔹 Link staff users to a company (nullable for customers)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="staff")

    # 🔹 Existing relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    tickets = relationship("Ticket", back_populates="user")
    payments = relationship("Payment", back_populates="user")



class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


# Bus tables

bus_routes = Table(
    "bus_routes",
    Base.metadata,

    Column("bus_id", String, ForeignKey("buses.id"), primary_key=True),
    Column("route_id", String, ForeignKey("routes.id"), primary_key=True)
)

class Bus(Base):
    __tablename__ = "buses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    plate_number = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)   # total seats
    available_seats = Column(Integer, nullable=False, default=0)  # changes when booking

    created_at = Column(DateTime, default=datetime.now(UTC))

    routes = relationship(
        "Route",
        secondary=bus_routes,
        back_populates="buses"
    )

    tickets = relationship("Ticket", back_populates="bus")
    company_id = Column(String, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="buses")

class Route(Base):
    __tablename__ = "routes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC))

    # many-to-many with buses
    buses = relationship(
        "Bus",
        secondary=bus_routes,
        back_populates="routes"
    )

    tickets = relationship("Ticket", back_populates="route")
    company_id = Column(String, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="routes")  


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    bus_id = Column(String, ForeignKey("buses.id"))
    route_id = Column(String, ForeignKey("routes.id"))
    company_id = Column(String, ForeignKey("companies.id"))  
    qr_code = Column(String, nullable=False)
    status = Column(String, default="booked")
    mode = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.now(UTC))

    user = relationship("User", back_populates="tickets")
    bus = relationship("Bus", back_populates="tickets")
    route = relationship("Route", back_populates="tickets")
    company = relationship("Company", back_populates="tickets")  
    payments = relationship("Payment", back_populates="ticket")

# The payment 

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    phone_number = Column(String(20), nullable=False) 
    amount = Column(Float, nullable=False)
    provider = Column(String(50), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    created_at = Column(DateTime, default=datetime.now(UTC))

    ticket = relationship("Ticket", back_populates="payments")
    user = relationship("User", back_populates="payments")


class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))

    staff = relationship("User", back_populates="company")  
    buses = relationship("Bus", back_populates="company")
    routes = relationship("Route", back_populates="company")
    tickets = relationship("Ticket", back_populates="company")  
