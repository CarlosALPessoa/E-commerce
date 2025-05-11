from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Livro
from schemas import LivroResponse

from typing import List


import schemas, models
import shutil, os

router = APIRouter()

@router.get("/livros", response_model=list[schemas.LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(Livro).all()

@router.get("/livros/{id}", response_model=LivroResponse)
def details_book(id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()

    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    livro.preco = round(livro.preco, 2)
    return livro

@router.post("/livros")
def criar_livro(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    novo_livro = models.Livro(**livro.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

@router.get("/livros_recomendacao/{user_id}")
def get_livros(user_id: int, categorias: List[str] = Query(default=[]), db: Session = Depends(get_db)):

    livros = db.query(Livro).filter(Livro.categoria.in_(categorias)).all()

    return livros