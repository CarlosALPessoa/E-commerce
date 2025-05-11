from sqlalchemy import Column, Integer, String, Float
from database import Base

class Livro(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(50), index=True)
    descricao = Column(String(50))
    preco = Column(Float)
    image = Column(String)
    categoria = Column(String)
    qtd = Column(Integer)
