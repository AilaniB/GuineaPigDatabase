from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Foster(Base):
    __tablename__ = "fosters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    email = Column(String(100), unique=False, nullable=False)
    phone_number = Column(String(20), unique=False, nullable=False)
    address = Column(String(100), unique=False, nullable=False)

    guineapig = relationship("GuineaPig", back_populates="foster")
