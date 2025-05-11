from fastapi import FastAPI
from database import Base, engine
from routers import router

import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
