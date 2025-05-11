from sqlalchemy import Column, Integer, String, Float
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)