from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import orm
from datetime import datetime, UTC
import uuid
import qrcode
import io
import base64
import json
import hmac
import hashlib
import os
from uuid import UUID

from dotenv import load_dotenv

from database.models import Ticket, User, Bus, Route
from schemas.TicketsScheme import TicketCreate, TicketResponse
from database.dbs import get_db 

from methods.functions import get_current_user
from methods.permissions import check_permission

router = APIRouter(prefix="/api/v1/tickets", tags=['Ticket Managment Endpoint'])
load_dotenv()
SECRET_KEY = os.environ.get("TICKET_SECRET_KEY") 
key_bytes = SECRET_KEY.encode()                    


async def generate_signed_qr(payload: dict) -> str:
    ticket_id = payload["ticket_id"].encode()  # only ticket_id
    signature = hmac.new(key_bytes, ticket_id, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(ticket_id + b"." + signature).decode()

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()

    return qr_base64, token


@router.post("/", response_model=TicketResponse, dependencies=[Depends(get_current_user)])
async def create_ticket(ticket_req: TicketCreate, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == str(ticket_req.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bus = db.query(Bus).filter(Bus.id == str(ticket_req.bus_id)).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    route = db.query(Route).filter(Route.id == str(ticket_req.route_id)).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Checking the if ticket is not assigned before
    
    existing_ticket = db.query(Ticket).filter(
        Ticket.user_id == str(ticket_req.user_id),
        Ticket.route_id == str(ticket_req.route_id),
        Ticket.status == "booked",  # or 'active' depending on your logic
        Ticket.mode == 'active'
    ).first()

    if existing_ticket:
        raise HTTPException(
            status_code=400,
            detail="You have already booked a ticket for this route"
        )

    
    payload = {
        "ticket_id": str(uuid.uuid4()),
        "user_id": str(ticket_req.user_id),
        "bus_id": str(ticket_req.bus_id),
        "route_id": str(ticket_req.route_id),
        "status": "Booked",
        "created_at": datetime.now(UTC).isoformat()
    }

    qr_base64, signed_token = await generate_signed_qr(payload)

    
    new_ticket = Ticket(
        id=payload["ticket_id"],
        user_id=str(ticket_req.user_id),
        bus_id=str(ticket_req.bus_id),
        route_id=str(ticket_req.route_id),
        qr_code=signed_token,
        status="booked",
        created_at=datetime.now(UTC),
        mode='active'
    )

    if bus.available_seats >= bus.capacity:
        raise HTTPException(status_code=404, detail="Bus is overloaded")
    
    bus.available_seats += 1
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return TicketResponse(
        id=new_ticket.id,
        user_id=new_ticket.user_id,
        qr_code=qr_base64,
        status=new_ticket.status,
        created_at=new_ticket.created_at,
        mode=new_ticket.mode
    )


# Endpoint to list tickets
@router.get("/", response_model=List[TicketResponse], dependencies=[Depends(get_current_user), Depends(check_permission("see_all_tickets"))])
def get_all_tickets(db: Session = Depends(get_db)):
    # Eagerly load the related user and route data in a single query
    tickets = db.query(Ticket).options(
        orm.joinedload(Ticket.user),
        orm.joinedload(Ticket.route),
        orm.joinedload(Ticket.bus)
    ).all()
    
    response_data = []
    for ticket in tickets:
        ticket_data = {
            "id": ticket.id,
            "user_id": str(ticket.user_id),
            "full_name": ticket.user.full_name if ticket.user else None,
            "qr_code": ticket.qr_code,
            "status": ticket.status,
            "created_at": ticket.created_at,
            "mode": ticket.mode,
            "route": {
                "origin": ticket.route.origin if ticket.route else None,
                "destination": ticket.route.destination if ticket.route else None,
                "price":ticket.route.price if ticket.route else None
            },
            "bus": ticket.bus.plate_number  if ticket.bus else None
        }
        response_data.append(ticket_data)
        
    return response_data

@router.get("/{ticket_id}", response_model=TicketResponse, dependencies=[Depends(get_current_user)])
async def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketResponse(
        id=ticket.id,
        user_id=ticket.user_id,
        qr_code=ticket.qr_code,
        status=ticket.status,
        created_at=ticket.created_at,
        mode=ticket.mode
    )

# Soft deleting the ticket by user

@router.put("/{ticket_id}", dependencies=[Depends(get_current_user)])
async def delete_ticket(ticket_id: str, db: Session = Depends(get_db)):
    # find ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # update status instead of hard deleting
    ticket.mode = "deleted"
    db.commit()
    db.refresh(ticket)

    return {"message": "Ticket  deleted", "ticket_id": str(ticket.id), "status": ticket.status}

@router.get("/users/{user_id}", response_model=list[TicketResponse], dependencies=[Depends(get_current_user)])
async def list_user_tickets(user_id: str, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(
        Ticket.user_id == str(user_id),
        Ticket.mode == 'active'
        ).all()
    response = []
    for t in tickets:
        # qr_base64, _ = generate_signed_qr({
        #     "ticket_id": t.id,
        #     "user_id": t.user_id,
        #     "bus_id": t.bus_id,
        #     "route_id": t.route_id,
        #     "created_at": t.created_at.isoformat()
        # })
        response.append(TicketResponse(
            id=t.id,
            user_id=t.user_id,
            qr_code=t.qr_code,
            status=t.status,
            created_at=t.created_at,
            mode=t.mode
        ))

    return response



@router.patch("/{ticket_id}/status", response_model=TicketResponse, dependencies=[Depends(get_current_user)])
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

@router.delete("/admin_delete/{ticket_id}", dependencies=[Depends(get_current_user)])
async def admin_delete_ticket(ticket_id: str, db: Session = Depends(get_db)):
    # find ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()


    return {"message": "Ticket deleted by admin"}