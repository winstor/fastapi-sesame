from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.db.database import database, Base
from fastapi.middleware.cors import CORSMiddleware
from app.api.app.v1.user_api import api_router as user_api_router
from app.api.app.v1.file_api import api_router as file_api_router
from app.core.jwt import oauth

database.set_default_connection('sesame')
database.create_all(base=Base)

oauth.secret_key = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e8'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
async def root():
    return ''


# 微信服务端  临时添加, 正式环境单独运行
# app.include_router(wechat_server_router, tags=['wechat server'])

app.include_router(user_api_router, prefix='/api')
# 文件服务
app.include_router(file_api_router, prefix='/api')

# uvicorn app.user:app --reload --port=8080
