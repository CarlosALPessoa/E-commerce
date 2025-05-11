from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class Sale(Base):
    __tablename__ = "Sale-transaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    items = Column(JSON, nullable=False)
    status_sale = Column(String, nullable=False, default="Pendente")