from fastapi import FastAPI, Depends, Request, HTTPException, Form, Body
from app.db.database import database
from app.api.workflow.v1.api import api_router
from app.extensions import site_sign
from app.api.workflow.db.database import Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import tifffile as tif

# 更换数据库
database.create_engine("sqlite:///./app/db/sql_workflow1.db", connect_args={"check_same_thread": False})
# 数据库表不存在并初始化
database.create_all(base=Base)

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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response


# 某某高校
site_id = 1
site_secret = '1133b733353411eb94b7d8cb8a079b7c'


class Login(BaseModel):
    username: str
    password: str


@app.get("/")
async def root():
    return "高校开发版本！"


@app.get("/tif")
async def tif():
    base_path = f"images/000001.tif"
    path = f"images/000002.png"
    im = tif.imread(base_path)
    tif.imsave(path, im)
    # im.thumbnail(im.size)
    # im.save(path, format='PNG')


# sign 获取站点登录授权签名
@app.get("/auth_sign")
async def get_sign():
    return site_sign.sign_encode(site_secret)


@app.post("/api/vue-element-admin/user/login")
async def user_login(data: Login):
    return {"code": 20000, "data": {"token": "admin-token", "token_type": "bearer"}}


# api版本v1
app.include_router(api_router, prefix='/api')

'''
运行 命令
uvicorn app.main:app --reload

'''

# uvicorn app.root:app --reload --port=8801

# uvicorn app.workflow:app --reload  --port=8000

# uvicorn app.workflow1:app --reload  --port=8001
