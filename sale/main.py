from fastapi import FastAPI
from database import Base, engine
from routers import router
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:5500"] se for mais seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)