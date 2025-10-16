from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Float, Enum, Boolean
from sqlalchemy.orm import relationship
from database.dbs import Base
import uuid
from datetime import datetime, UTC
import enum



# roles <-> permissions (many-to-many)
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", String, ForeignKey("permissions.id"), primary_key=True),
)

# users <-> roles (many-to-many)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
)

# buses <-> routes (many-to-many)
bus_routes = Table(
    "bus_routes",
    Base.metadata,
    Column("bus_id", String, ForeignKey("buses.id"), primary_key=True),
    Column("route_id", String, ForeignKey("routes.id"), primary_key=True)
)

# buses <-> schedules (many-to-many)
bus_schedules = Table(
    "bus_schedules",
    Base.metadata,
    Column("bus_id", String, ForeignKey("buses.id"), primary_key=True),
    Column("schedule_id", String, ForeignKey("schedules.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="staff")

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    tickets = relationship("Ticket", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Role(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    phone_number = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    provider = Column(String(50), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    created_at = Column(DateTime, default=datetime.now(UTC))

    ticket = relationship("Ticket", back_populates="payments")
    user = relationship("User", back_populates="payments")

# Comapny model
class Company(Base):
    __tablename__ = "companies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    # is_verfied = Column(Boolean, default=False)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))


    staff = relationship("User", back_populates="company")
    buses = relationship("Bus", back_populates="company")
    routes = relationship("Route", back_populates="company")
    route_segments = relationship("RouteSegment", back_populates="company")
    stations = relationship("BusStation", back_populates="company")
    schedules = relationship("Schedule", back_populates="company")
    tickets = relationship("Ticket", back_populates="company")

# Bus model
class Bus(Base):
    __tablename__ = "buses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    plate_number = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now(UTC))
    company_id = Column(String, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="buses")
    schedules = relationship("Schedule", back_populates="bus")
    tickets = relationship("Ticket", back_populates="bus")
    routes = relationship("Route", secondary=bus_routes, back_populates="buses")

# Bus station model
class BusStation(Base):
    __tablename__ = "bus_stations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    company_id = Column(String, ForeignKey("companies.id"))
    created_at = Column(DateTime, default=datetime.now(UTC))

    

    company = relationship("Company", back_populates="stations")
    route_segments_from = relationship("RouteSegment", back_populates="start_station", foreign_keys="RouteSegment.start_station_id")
    route_segments_to = relationship("RouteSegment", back_populates="end_station", foreign_keys="RouteSegment.end_station_id")

# -----------------------------
# Route (overall route)
# -----------------------------
class Route(Base):
    __tablename__ = "routes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # name = Column(String, nullable=False)
    origin_id = Column(String, ForeignKey("bus_stations.id"))
    destination_id = Column(String, ForeignKey("bus_stations.id"))
    price = Column(Float, nullable=False)  # overall route price
    company_id = Column(String, ForeignKey("companies.id"))
    created_at = Column(DateTime, default=datetime.now(UTC))

    company = relationship("Company", back_populates="routes")
    segments = relationship("RouteSegment", back_populates="route")
    buses = relationship("Bus", secondary=bus_routes, back_populates="routes")
    tickets = relationship("Ticket", back_populates='route')

# -----------------------------
# RouteSegment (segment between two stations)
# -----------------------------
class RouteSegment(Base):
    __tablename__ = "route_segments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    route_id = Column(String, ForeignKey("routes.id"), nullable=False)
    start_station_id = Column(String, ForeignKey("bus_stations.id"), nullable=False)
    end_station_id = Column(String, ForeignKey("bus_stations.id"), nullable=False)
    price = Column(Float, nullable=False)
    stop_order = Column(Integer, nullable=False)
    company_id = Column(String, ForeignKey("companies.id"))

    route = relationship("Route", back_populates="segments")
    start_station = relationship("BusStation", back_populates="route_segments_from", foreign_keys=[start_station_id])
    end_station = relationship("BusStation", back_populates="route_segments_to", foreign_keys=[end_station_id])
    schedules = relationship("Schedule", back_populates="route_segment")
    company = relationship("Company", back_populates="route_segments")

# -----------------------------
# Schedule
# -----------------------------
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    bus_id = Column(String, ForeignKey("buses.id"))
    route_segment_id = Column(String, ForeignKey("route_segments.id"))
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=True)
    company_id = Column(String, ForeignKey("companies.id"))

    bus = relationship("Bus", back_populates="schedules")
    route_segment = relationship("RouteSegment", back_populates="schedules")
    company = relationship("Company", back_populates="schedules")
    tickets = relationship("Ticket", back_populates="schedule")
    buses = relationship("Bus", secondary=bus_schedules, back_populates="schedules")

# -----------------------------
# Ticket
# -----------------------------
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    bus_id = Column(String, ForeignKey("buses.id"))
    schedule_id = Column(String, ForeignKey("schedules.id"))
    company_id = Column(String, ForeignKey("companies.id"))
    route_id = Column(String, ForeignKey("routes.id"))
    qr_code = Column(String, nullable=False)
    status = Column(String, default="booked")
    mode = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.now(UTC))

    user = relationship("User", back_populates="tickets")
    bus = relationship("Bus", back_populates="tickets")
    schedule = relationship("Schedule", back_populates="tickets")
    company = relationship("Company", back_populates="tickets")
    payments = relationship("Payment", back_populates="ticket")
    route = relationship("Route", back_populates='tickets')
