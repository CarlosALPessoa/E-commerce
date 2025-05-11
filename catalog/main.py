from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from routers import router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import json
import httpx as client

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# static_dir = os.path.join(BASE_DIR, "static", "img")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:5500"] se for mais seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def livros_data():
    """Carrega os dados de livros a partir de um arquivo JSON"""
    with open("livros.json", "r", encoding="utf-8") as file:
        return json.load(file)
        

def created_livros_ids():
    for livro in livros_data():
        response = client.post("/livros", json=livro)
        assert response.status_code in (200, 201), f"Erro ao criar livro: {livro['titulo']}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
