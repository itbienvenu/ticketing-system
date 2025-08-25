from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.dbs import get_db
from database.models import Ticket, Payment, PaymentStatus, Route
from schemas.PaymentScheme import PaymentCreate, PaymentResponse
from methods.functions import get_current_user 
from uuid  import UUID, uuid4
router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
def initiate_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # 1. Verify ticket exists
    ticket = db.query(Ticket).filter(Ticket.id == str(payment.ticket_id)).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")


    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only pay for your own ticket")

    get_route = db.query(Route).filter(Route.id == ticket.route_id).first()
    # 3. Create Payment record

    ticket.status = "pending payment"
    new_payment = Payment(
        id=str(uuid4()),
        ticket_id=str(ticket.id),
        user_id=str(current_user.id),
        phone_number=str(payment.phone_number),
        provider=str(payment.provider.value),
        amount=int(get_route.price), 
        status=PaymentStatus.pending,
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    # TODO: call external payment api

    return new_payment
