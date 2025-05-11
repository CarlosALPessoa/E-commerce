from pydantic import BaseModel

class LivroCreate(BaseModel):
    titulo: str
    descricao: str
    preco: float
    image: str
    categoria: str
    qtd: int

class LivroResponse(LivroCreate):
    id: int

    class Config:
        orm_mode = True