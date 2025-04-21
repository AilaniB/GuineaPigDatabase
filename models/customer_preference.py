from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class CustomerPreference(Base):
    __tablename__ = "customer_preference"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    max_age = Column(Integer, nullable=True)
    min_age = Column(Integer, nullable=True)
    bonded = Column(Boolean, default=False)
    max_group_size = Column(Integer, nullable=True)