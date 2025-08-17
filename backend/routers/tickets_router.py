from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, UTC
import uuid
import qrcode
import io
import base64
import json
import hmac
import hashlib
import os

from dotenv import load_dotenv

from database.models import Ticket, User, Bus, Route
from schemas.TicketsScheme import TicketCreate, TicketResponse
from database.dbs import get_db 

router = APIRouter(prefix="/api/v1/tickets", tags=['Ticket Managment Endpoint'])
load_dotenv()
SECRET_KEY = os.environ.get("TICKET_SECRET_KEY") 
key_bytes = SECRET_KEY.encode()                    # convert to bytes


def generate_signed_qr(payload: dict) -> str:
    # create HMAC signature
    data = json.dumps(payload, separators=(',', ':')).encode()
    signature = hmac.new(key_bytes, data, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(data + b"." + signature).decode()

    # generate QR image as base64
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    return qr_base64, token



@router.post("/", response_model=TicketResponse)
def create_ticket(ticket_req: TicketCreate, db: Session = Depends(get_db)):
    # Validate user, bus, route existence
    user = db.query(User).filter(User.id == str(ticket_req.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bus = db.query(Bus).filter(Bus.id == str(ticket_req.bus_id)).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    route = db.query(Route).filter(Route.id == str(ticket_req.route_id)).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Prepare payload for QR code (do NOT expose bus/route directly to client)
    payload = {
        "ticket_id": str(uuid.uuid4()),
        "user_id": str(ticket_req.user_id),
        "bus_id": str(ticket_req.bus_id),
        "route_id": str(ticket_req.route_id),
        "created_at": datetime.now(UTC).isoformat()
    }

    qr_base64, signed_token = generate_signed_qr(payload)

    # Save ticket to DB
    new_ticket = Ticket(
        id=payload["ticket_id"],
        user_id=str(ticket_req.user_id),
        bus_id=str(ticket_req.bus_id),
        route_id=str(ticket_req.route_id),
        qr_code=signed_token,
        status="booked",
        created_at=datetime.now(UTC)
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return TicketResponse(
        id=new_ticket.id,
        user_id=new_ticket.user_id,
        qr_code=qr_base64,
        status=new_ticket.status,
        created_at=new_ticket.created_at
    )



@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Return only QR code + minimal info
    qr_base64, _ = generate_signed_qr({
        "ticket_id": ticket.id,
        "user_id": ticket.user_id,
        "bus_id": ticket.bus_id,
        "route_id": ticket.route_id,
        "created_at": ticket.created_at.isoformat()
    })

    return TicketResponse(
        id=ticket.id,
        user_id=ticket.user_id,
        qr_code=qr_base64,
        status=ticket.status,
        created_at=ticket.created_at
    )



@router.get("/users/{user_id}", response_model=list[TicketResponse])
def list_user_tickets(user_id: str, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.user_id == str(user_id)).all()
    response = []
    for t in tickets:
        qr_base64, _ = generate_signed_qr({
            "ticket_id": t.id,
            "user_id": t.user_id,
            "bus_id": t.bus_id,
            "route_id": t.route_id,
            "created_at": t.created_at.isoformat()
        })
        response.append(TicketResponse(
            id=t.id,
            user_id=t.user_id,
            qr_code=qr_base64,
            status=t.status,
            created_at=t.created_at
        ))
    return response



@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(ticket_id: str, status: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = status
    db.commit()
    db.refresh(ticket)

    qr_base64, _ = generate_signed_qr({
        "ticket_id": ticket.id,
        "user_id": ticket.user_id,
        "bus_id": ticket.bus_id,
        "route_id": ticket.route_id,
        "created_at": ticket.created_at.isoformat()
    })

    return TicketResponse(
        id=ticket.id,
        user_id=ticket.user_id,
        qr_code=qr_base64,
        status=ticket.status,
        created_at=ticket.created_at
    )
