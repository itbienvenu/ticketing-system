from pydantic import BaseModel, constr, Field
from enum import Enum

from uuid import UUID

class PaymentProvider(str, Enum):
    momo = "momo"
    tigocash = "tigocash"

class PaymentCreate(BaseModel):
    ticket_id: UUID
    phone_number: str
    provider: PaymentProvider

class PaymentResponse(BaseModel):
    id: str
    ticket_id: str
    user_id: str
    phone_number: str
    amount: float
    provider: str
    status: str

    class Config:
        from_attributes = True