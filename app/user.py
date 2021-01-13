from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.db.database import database, Base
from fastapi.middleware.cors import CORSMiddleware
from app.api.app.v1.user_api import api_router as user_api_router
from app.api.app.v1.file_api import api_router as file_api_router
# from app.api.app.v1.wechat_server_api import api_router as wechat_server_router
from app.extensions import site_sign

database.set_default_connection('local')
database.create_all(base=Base)

app = FastAPI()

site_secret = '1133b733353411eb94b7d8cb8a079b7c'

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


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTMzYjczMzM1MzQxMWViOTRiN2Q4Y2I4YTA3OWI3YyIsImV4cCI6MTc2MjgzMDg4MX0.MzbZr7jC7O5Pw0Y2HjZKZC2Uu5rHw-gTIggSACMU5c4

@app.get("/")
async def root():
    return site_sign.sign_encode(site_secret)


# 微信服务端  临时添加, 正式环境单独运行
# app.include_router(wechat_server_router, tags=['wechat server'])

app.include_router(user_api_router, prefix='/api')
# 文件服务
app.include_router(file_api_router, prefix='/api')

# uvicorn app.user:app --reload --port=8080
