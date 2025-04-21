from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    id: int
    name: str
    age: int
    email: str
    phone_number: str
    address: str

class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    class Config:
        from_attributes = True