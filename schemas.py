from pydantic import BaseModel
from typing import Optional
from datetime import date


class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = ""
    addr: Optional[str] = ""
    lprice: Optional[float] = 0
    dprice: Optional[float] = 0
    lunch: Optional[bool] = True
    dinner: Optional[bool] = True


class CustomerOut(BaseModel):
    id: int
    name: str
    phone: str
    addr: str
    lprice: float
    dprice: float
    lunch: bool
    dinner: bool
    model_config = {"from_attributes": True}


class EntryUpsert(BaseModel):
    customer_id: int
    date: date
    lunch: Optional[int] = 0
    dinner: Optional[int] = 0


class EntryOut(BaseModel):
    id: int
    customer_id: int
    date: date
    lunch: int
    dinner: int
    model_config = {"from_attributes": True}


class PaymentToggle(BaseModel):
    customer_id: int
    year: int
    month: int


class PaymentOut(BaseModel):
    customer_id: int
    year: int
    month: int
    paid: bool