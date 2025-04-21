from pydantic import BaseModel
from typing import Optional

class GuineaPigBase(BaseModel):
    id: int
    name: str
    age: int
    bonded: bool
    foster_id: int
    customer_id: int

class GuineaPigCreate(GuineaPigBase):
    pass

class GuineaPigResponse(GuineaPigBase):
    class Config:
        from_attributes = True

