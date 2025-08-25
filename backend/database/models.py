from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Float, Enum
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.dbs import Base
import uuid
from datetime import datetime, UTC
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC))

    tickets = relationship("Ticket", back_populates="user")
    payments = relationship("Payment", back_populates="user")

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
    created_at = Column(DateTime, default=datetime.now(UTC))

    # many-to-many with routes
    routes = relationship(
        "Route",
        secondary=bus_routes,
        back_populates="buses"
    )

    tickets = relationship("Ticket", back_populates="bus")

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


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    bus_id = Column(String, ForeignKey("buses.id"))
    route_id = Column(String, ForeignKey("routes.id")) 
    qr_code = Column(String, nullable=False)
    status = Column(String, default="booked")
    mode = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.now(UTC))

    user = relationship("User", back_populates="tickets")
    bus = relationship("Bus", back_populates="tickets")
    route = relationship("Route", back_populates="tickets")  # link to Route
    payments = relationship("Payment", back_populates="ticket") # link to payments tble

# The payment 

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    phone_number = Column(String(20), nullable=False) 
    amount = Column(Float, nullable=False)
    provider = Column(String(50), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    created_at = Column(DateTime, default=datetime.now(UTC))

    ticket = relationship("Ticket", back_populates="payments")
    user = relationship("User", back_populates="payments")