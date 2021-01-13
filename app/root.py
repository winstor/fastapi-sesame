from fastapi import FastAPI, Request
from .db.database import database
from app.api.app.v1.root_api import api_router
from app.core import security


database.create_all()

app = FastAPI()


@app.middleware("http")
async def root_security(request: Request, call_next):
    # token SECRET_KEY
    security.SECRET_KEY = "19d25e094faa6ca2556c881155b7a9563b93f7099f6f0f4caa6cf63b88e8d3e1-root"
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return "高校开发版本！"


app.include_router(api_router, prefix='/api')


# uvicorn app.root:app --reload --port=8888
