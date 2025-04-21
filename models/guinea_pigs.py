from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from database import Base

class GuineaPig(Base):
    __tablename__ = "guineapig"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    age = Column(Integer)
    bonded = Column(Boolean, default=False)
    foster_id = Column(Integer, ForeignKey("fosters.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    foster = relationship("Foster", back_populates="guineapig")
    customer = relationship("Customer", back_populates="guineapig")





