from pydantic import BaseModel
from typing import Optional

class FosterBase(BaseModel):
    id: int
    name: str
    age: int
    email: str
    phone_number: str
    address: str

class FosterCreate(FosterBase):
    pass


class FosterResponse(FosterBase):
    class Config:
        from_attributes = True